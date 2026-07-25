import pandas as pd

from src.file_utils import load_object

# Load cleaned dataset
df = pd.read_csv("data/processed/marketing_cleaned.csv")

# Features used by KMeans
model_features = [
    "Income",
    "Total_Spending",
    "Total_Purchases",
    "Recency",
    "NumWebVisitsMonth",
    "Total_Promo_Accepted",
    "Children"
]

# Load scaler
preprocessor = load_object(
    "artifacts/data_transformation/preprocessor.pkl"
)

# Load trained model
model = load_object(
    "artifacts/model_trainer/kmeans_model.pkl"
)

# Scale data
X = preprocessor.transform(df[model_features])

# Predict cluster
df["Cluster"] = model.predict(X)

# Cluster profile
profile = (
    df
    .groupby("Cluster")[model_features]
    .mean()
    .round(2)
)

print("\nCluster Profiles\n")
print(profile)

# Save for future use
profile.to_csv(
    "artifacts/model_trainer/segment_profiles.csv"
)

print("\nSaved Successfully!")