
import streamlit as st
import pandas as pd
from datetime import datetime
from src.predict import predict_customer_churn


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# --------------------------------------------------

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "latest_prediction" not in st.session_state:
    st.session_state.latest_prediction = None


# --------------------------------------------------
# 3. APPLICATION HEADER
# --------------------------------------------------

st.title("📊 Customer Churn Prediction")

st.caption(
    "Machine Learning Based Customer Retention "
    "and Analytics Dashboard"
)

st.divider()


# --------------------------------------------------
# 4. CUSTOMER INPUT FORM
# --------------------------------------------------

st.subheader("👤 Customer Information")

with st.form("customer_prediction_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Personal Information")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

    with col2:
        st.markdown("### Account Information")

        tenure = st.number_input(
            "Tenure (Months)",
            min_value=0,
            max_value=72,
            value=12
        )

        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    with col3:
        st.markdown("### Billing Information")

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=840.0
        )

    st.divider()

    st.subheader("📡 Services Information")

    service_col1, service_col2, service_col3 = st.columns(3)

    with service_col1:

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

    with service_col2:

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

    with service_col3:

        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

    st.divider()

    predict_button = st.form_submit_button(
        "🔍 Predict Customer Churn",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# 5. CUSTOMER PREDICTION
# --------------------------------------------------

if predict_button:

    customer_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:

        result = predict_customer_churn(customer_data)

        probability = result["churn_probability"]

        prediction_record = {
            "Prediction Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Gender": gender,
            "Senior Citizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "Tenure": tenure,
            "Contract": contract,
            "Monthly Charges": monthly_charges,
            "Total Charges": total_charges,
            "Internet Service": internet_service,
            "Payment Method": payment_method,
            "Prediction": result["prediction"],
            "Churn Probability": round(probability * 100, 2)
        }

        st.session_state.prediction_history.append(
            prediction_record
        )

        st.session_state.latest_prediction = {
            "prediction": result["prediction"],
            "probability": probability,
            "customer": customer_data.copy()
        }

    except Exception as error:

        st.error("Unable to generate prediction.")
        st.exception(error)


# --------------------------------------------------
# 6. LATEST PREDICTION RESULT
# --------------------------------------------------

if st.session_state.latest_prediction:

    latest = st.session_state.latest_prediction

    st.divider()
    st.subheader("🎯 Latest Prediction Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        if latest["prediction"] == "Churn":

            st.error(
                "⚠️ Customer is likely to Churn"
            )

        else:

            st.success(
                "✅ Customer is likely to Stay"
            )

    with result_col2:

        st.metric(
            "Churn Probability",
            f"{latest['probability'] * 100:.2f}%"
        )

    st.progress(latest["probability"])

    st.caption(
        "This is a machine learning estimate, "
        "not a guarantee of actual customer behavior."
    )


    # --------------------------------------------------
    # 7. RETENTION RECOMMENDATIONS
    # --------------------------------------------------

    st.divider()

    st.subheader("💡 Customer Retention Recommendations")

    customer = latest["customer"]

    if latest["prediction"] == "Churn":

        st.warning(
            "This customer has been classified as likely to churn."
        )

        recommendations = []

        if customer["Contract"] == "Month-to-month":

            recommendations.append(
                "Offer an incentive to upgrade to a long-term contract."
            )

        if customer["tenure"] <= 12:

            recommendations.append(
                "Provide a new-customer loyalty offer."
            )

        if customer["PaymentMethod"] == "Electronic check":

            recommendations.append(
                "Encourage automatic payment options."
            )

        if customer["TechSupport"] == "No":

            recommendations.append(
                "Offer technical support assistance."
            )

        if customer["OnlineSecurity"] == "No":

            recommendations.append(
                "Offer an online security package."
            )

        if customer["InternetService"] == "Fiber optic":

            recommendations.append(
                "Review the customer's internet plan and pricing."
            )

        if not recommendations:

            recommendations.append(
                "Contact the customer and understand their concerns."
            )

        for recommendation in recommendations:

            st.write(f"• {recommendation}")

    else:

        st.success(
            "This customer is predicted to stay. "
            "Continue providing good service and customer engagement."
        )


# --------------------------------------------------
# 8. ANALYTICS DASHBOARD
# --------------------------------------------------

st.divider()

st.header("📈 Customer Analytics Dashboard")

if st.session_state.prediction_history:

    history_df = pd.DataFrame(
        st.session_state.prediction_history
    )

    total_customers = len(history_df)

    churned_customers = (
        history_df["Prediction"] == "Churn"
    ).sum()

    stayed_customers = (
        history_df["Prediction"] == "Stay"
    ).sum()

    churn_percentage = (
        churned_customers / total_customers
    ) * 100

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Customers",
        total_customers
    )

    metric2.metric(
        "Likely to Churn",
        int(churned_customers)
    )

    metric3.metric(
        "Likely to Stay",
        int(stayed_customers)
    )

    metric4.metric(
        "Predicted Churn Rate",
        f"{churn_percentage:.2f}%"
    )


    # --------------------------------------------------
    # 9. CHURN DISTRIBUTION CHART
    # --------------------------------------------------

    st.subheader("Customer Churn Distribution")

    chart_data = pd.DataFrame({
        "Customer Status": ["Churn", "Stay"],
        "Number of Customers": [
            churned_customers,
            stayed_customers
        ]
    })

    st.bar_chart(
        chart_data,
        x="Customer Status",
        y="Number of Customers"
    )


    # --------------------------------------------------
    # 10. PREDICTION HISTORY
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Prediction History")

    filter_option = st.selectbox(
        "Filter Predictions",
        ["All", "Churn", "Stay"],
        key="history_filter"
    )

    if filter_option == "Churn":

        filtered_history = history_df[
            history_df["Prediction"] == "Churn"
        ]

    elif filter_option == "Stay":

        filtered_history = history_df[
            history_df["Prediction"] == "Stay"
        ]

    else:

        filtered_history = history_df

    st.dataframe(
        filtered_history,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # 11. CSV DOWNLOAD
    # --------------------------------------------------

    csv_data = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download All Prediction Records",
        data=csv_data,
        file_name="customer_churn_predictions.csv",
        mime="text/csv",
        key="download_history_btn"
    )


    # --------------------------------------------------
    # 12. CLEAR HISTORY
    # --------------------------------------------------

    if st.button(
        "🗑️ Clear Prediction History",
        key="clear_history_btn"
    ):

        st.session_state.prediction_history.clear()

        st.session_state.latest_prediction = None

        st.rerun()

else:

    st.info(
        "No customer predictions available yet. "
        "Enter customer details above to get started."
    )


# --------------------------------------------------
# 13. APPLICATION FOOTER
# --------------------------------------------------


st.subheader("🤖 Model Performance")

st.write("**Logistic Regression — Test Set Results**")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.metric("Accuracy", "80.45%")
col2.metric("ROC-AUC", "0.8359")
col3.metric("Churn Recall", "57.49%")
col4.metric("Churn F1-Score", "0.61")

st.write(
    "The Logistic Regression model was selected based on its "
    "overall accuracy and ROC-AUC. Balanced Logistic Regression "
    "is an alternative when prioritizing churn recall."
)

st.caption(
    "Customer Churn Prediction | Machine Learning Project | "
    "Powered by Python, Scikit-learn and Streamlit"
)
