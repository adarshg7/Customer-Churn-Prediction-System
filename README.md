# Customer Churn Prediction System

## Overview
End-to-end ML system to predict telecom customer churn using FastAPI and Streamlit.

## Features
- Feature-engineered churn model
- Real-time prediction API
- Interactive frontend UI
- City-level encoding
- Deployment-ready

## Tech Stack
- Python, Scikit-learn
- FastAPI
- Streamlit
- Pandas, NumPy

## How to Run Locally
```bash
uvicorn app.main:app --reload
streamlit run frontend/frontend.py
