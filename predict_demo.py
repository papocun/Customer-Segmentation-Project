from src.pipeline.predict_pipeline import (
    CustomerData,
    PredictPipeline
)

customer = CustomerData(

    Income=50000,

    Total_Spending=1200,

    Total_Purchases=20,

    Recency=10,

    NumWebVisitsMonth=5,

    Total_Promo_Accepted=2,

    Children=1

)

df = customer.get_data_as_dataframe()

pipeline = PredictPipeline()

prediction = pipeline.predict(df)

print()

print("="*50)

print("Predicted Cluster :", prediction[0])

print("="*50)