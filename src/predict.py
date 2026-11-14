
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

loaded_model = joblib.load(BASE_DIR / "models" / "best_churn_model.pkl")
loaded_encoder = joblib.load(BASE_DIR / "models" / "encoder.pkl")
loaded_scaler = joblib.load(BASE_DIR / "models" / "scaler.pkl")

CONTINUOUS_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "gender", "Partner", "Dependents", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod"
]


def predict_customer_churn(customer_data):
    customer_df = pd.DataFrame([customer_data])

    scaled_data = loaded_scaler.transform(
        customer_df[CONTINUOUS_FEATURES]
    )

    encoded_data = loaded_encoder.transform(
        customer_df[CATEGORICAL_FEATURES]
    )

    scaled_df = pd.DataFrame(
        scaled_data, columns=CONTINUOUS_FEATURES
    )

    encoded_df = pd.DataFrame(
        encoded_data,
        columns=loaded_encoder.get_feature_names_out(
            CATEGORICAL_FEATURES
        )
    )

    transformed_data = pd.concat(
        [
            customer_df[["SeniorCitizen"]].reset_index(drop=True),
            scaled_df,
            encoded_df
        ],
        axis=1
    )

    transformed_data = transformed_data.reindex(
        columns=loaded_model.feature_names_in_,
        fill_value=0
    )

    prediction = loaded_model.predict(transformed_data)[0]

    yes_index = list(loaded_model.classes_).index("Yes")
    churn_probability = loaded_model.predict_proba(
        transformed_data
    )[0][yes_index]

    return {
        "prediction": "Churn" if prediction == "Yes" else "Stay",
        "churn_probability": round(float(churn_probability), 4)
    }

