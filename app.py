"""
FastAPI Application
Customer Segmentation Prediction API
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.pipeline.predict_pipeline import (
    PredictPipeline,
    CustomerData
)

# ==========================================================
# FastAPI Initialization
# ==========================================================

app = FastAPI(
    title="Customer Segmentation API",
    description="Predict customer segments using a trained KMeans model.",
    version="1.0.0"
)

# ==========================================================
# Request Schema
# ==========================================================


class CustomerInput(BaseModel):
    Income: float
    Total_Spending: float
    Total_Purchases: float
    Recency: int
    NumWebVisitsMonth: int
    Total_Promo_Accepted: int
    Children: int


# ==========================================================
# Segment Mapping
# ==========================================================

SEGMENT_MAPPING = {
    0: {
        "segment": "High Value Customer",
        "description": (
            "Customers with high income, high spending, "
            "frequent purchases and strong promotional engagement."
        )
    },
    1: {
        "segment": "Budget Customer",
        "description": (
            "Customers with lower spending, fewer purchases "
            "and low promotional engagement."
        )
    }
}


# ==========================================================
# Home Route
# ==========================================================

@app.get("/")
async def home():

    return {
        "message": "Customer Segmentation API is running.",
        "status": "success"
    }


import traceback

# ==========================================================
# Prediction Route
# ==========================================================

@app.post("/predict")
async def predict(customer: CustomerInput):

    try:

        customer_data = CustomerData(

            Income=customer.Income,
            Total_Spending=customer.Total_Spending,
            Total_Purchases=customer.Total_Purchases,
            Recency=customer.Recency,
            NumWebVisitsMonth=customer.NumWebVisitsMonth,
            Total_Promo_Accepted=customer.Total_Promo_Accepted,
            Children=customer.Children

        )

        dataframe = customer_data.get_data_as_dataframe()

        pipeline = PredictPipeline()

        prediction = pipeline.predict(dataframe)

        cluster = int(prediction[0])

        result = SEGMENT_MAPPING.get(
            cluster,
            {
                "segment": "Unknown",
                "description": "No description available."
            }
        )

        return {
            "status": "success",
            "cluster": cluster,
            "segment": result["segment"],
            "description": result["description"]
        }

    except Exception as e:

        print("\n" + "=" * 70)
        print("❌ ERROR INSIDE /predict")
        print("=" * 70)
        traceback.print_exc()
        print("=" * 70 + "\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )