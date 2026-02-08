from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import numpy as np
from schemas import ChurnInput

app = FastAPI()

# ================= LOAD ARTIFACTS =================
model = joblib.load("model/trained_model.pkl")
feature_order = joblib.load("model/model_features.pkl")
city_map = joblib.load("model/city_map.pkl")
GLOBAL_CITY_MEAN = np.mean(list(city_map.values()))

# ================= COLUMN NAME MAP =================
COLUMN_MAP = {
    "Gender": "Gender",
    "Senior_Citizen": "Senior Citizen",
    "Partner": "Partner",
    "Dependents": "Dependents",
    "Tenure_Months": "Tenure Months",
    "Monthly_Charges": "Monthly Charges",
    "Total_Charges": "Total Charges",
    "Phone_Service": "Phone Service",
    "Multiple_Lines": "Multiple Lines",
    "Online_Security": "Online Security",
    "Online_Backup": "Online Backup",
    "Device_Protection": "Device Protection",
    "Tech_Support": "Tech Support",
    "Streaming_TV": "Streaming TV",
    "Streaming_Movies": "Streaming Movies",
    "Contract": "Contract",
    "Paperless_Billing": "Paperless Billing",
    "Internet_Service_DSL": "Internet Service_DSL",
    "Internet_Service_Fiber_optic": "Internet Service_Fiber optic",
    "Internet_Service_No": "Internet Service_No",
    "Payment_Method_Bank_transfer_automatic": "Payment Method_Bank transfer (automatic)",
    "Payment_Method_Credit_card_automatic": "Payment Method_Credit card (automatic)",
    "Payment_Method_Electronic_check": "Payment Method_Electronic check",
    "Payment_Method_Mailed_check": "Payment Method_Mailed check",
}

# ================= FEATURE ENGINEERING =================
def build_features(data: dict) -> pd.DataFrame:
    tm = data["Tenure_Months"]
    mc = data["Monthly_Charges"]
    tc = data["Total_Charges"]

    engineered = {
        "Tenure_Pee_Dollar": tm / (mc + 1),
        "Avg_Historical_Monthly": tc / (tm + 1),
        "Price_Hike_Indicator": mc / ((tc / (tm + 1)) + 1),
    }

    service_cols = [
        data["Phone_Service"], data["Multiple_Lines"], data["Online_Security"],
        data["Online_Backup"], data["Device_Protection"], data["Tech_Support"],
        data["Streaming_TV"], data["Streaming_Movies"]
    ]

    engineered["Total_Services"] = sum(service_cols)
    engineered["Cost_Per_Service"] = (
        mc / engineered["Total_Services"]
        if engineered["Total_Services"] > 0 else mc
    )

    city = data["City"].strip().title()
    engineered["City_Encoded"] = city_map.get(city, GLOBAL_CITY_MEAN)

    # IMPORTANT: Cluster dropped for inference consistency
    engineered["Cluster_Labels"] = -1

    base = {}
    for k, v in data.items():
        if k in COLUMN_MAP:
            base[COLUMN_MAP[k]] = v

    full = {**base, **engineered}
    df = pd.DataFrame([full])

    return df.reindex(columns=feature_order, fill_value=0)

# ================= API =================
@app.post("/predict")
async def predict(customer: ChurnInput):
    try:
        raw = customer.dict()
        X = build_features(raw)

        prob = model.predict_proba(X)[0][1]

        return {
            "probability": round(float(prob), 4),
            "risk": "High" if prob >= 0.5 else "Low"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
