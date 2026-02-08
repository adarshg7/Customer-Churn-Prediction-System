import streamlit as st
import requests

st.set_page_config("Churn Pro", layout="wide")
st.title("📉 Customer Churn Prediction")

with st.form("form"):
    city = st.text_input("City", "Los Angeles")
    gender = st.selectbox("Gender", [1, 0], format_func=lambda x: "Male" if x else "Female")
    senior = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    partner = st.selectbox("Partner", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    dependents = st.selectbox("Dependents", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    tenure = st.number_input("Tenure Months", 0, 100, 12)

    phone = st.selectbox("Phone Service", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    multi = st.selectbox("Multiple Lines", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    security = st.selectbox("Online Security", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    backup = st.selectbox("Online Backup", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    protection = st.selectbox("Device Protection", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    support = st.selectbox("Tech Support", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    tv = st.selectbox("Streaming TV", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    movies = st.selectbox("Streaming Movies", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")

    contract = st.selectbox("Contract", [0, 1, 2])
    paperless = st.selectbox("Paperless Billing", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    monthly = st.number_input("Monthly Charges", value=70.0)
    total = st.number_input("Total Charges", value=1000.0)

    internet = st.selectbox("Internet", ["DSL", "Fiber optic", "No"])
    payment = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "City": city,
        "Gender": gender,
        "Senior_Citizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "Tenure_Months": tenure,
        "Monthly_Charges": monthly,
        "Total_Charges": total,
        "Phone_Service": phone,
        "Multiple_Lines": multi,
        "Online_Security": security,
        "Online_Backup": backup,
        "Device_Protection": protection,
        "Tech_Support": support,
        "Streaming_TV": tv,
        "Streaming_Movies": movies,
        "Contract": contract,
        "Paperless_Billing": paperless,
        "Internet_Service_DSL": 1 if internet == "DSL" else 0,
        "Internet_Service_Fiber_optic": 1 if internet == "Fiber optic" else 0,
        "Internet_Service_No": 1 if internet == "No" else 0,
        "Payment_Method_Electronic_check": 1 if payment == "Electronic check" else 0,
        "Payment_Method_Mailed_check": 1 if payment == "Mailed check" else 0,
        "Payment_Method_Bank_transfer_automatic": 1 if "Bank" in payment else 0,
        "Payment_Method_Credit_card_automatic": 1 if "Credit" in payment else 0,
    }

    res = requests.post("http://127.0.0.1:8000/predict", json=payload)

    if res.status_code == 200:
        out = res.json()
        st.metric("Churn Probability", f"{out['probability']*100:.2f}%")
        st.write("Risk Level:", out["risk"])
