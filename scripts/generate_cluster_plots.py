import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from src.file_utils import load_object

# Load data and trained objects
df = pd.read_csv("data/processed/marketing_cleaned.csv")
preprocessor = load_object("artifacts/data_transformation/preprocessor.pkl")
model = load_object("artifacts/model_trainer/kmeans_model.pkl")

features = [
    "Income",
    "Total_Spending",
    "Total_Purchases",
    "Recency",
    "NumWebVisitsMonth",
    "Total_Promo_Accepted",
    "Children"
]

X_scaled = preprocessor.transform(df[features])
clusters = model.predict(X_scaled)
df["Cluster"] = clusters
df["Segment"] = df["Cluster"].map({0: "High Value Customer", 1: "Budget Customer"})

os.makedirs("images", exist_ok=True)

# Set styling
sns.set_theme(style="whitegrid")
palette = {0: "#10B981", 1: "#EF4444"}

# 1. Income vs Total Spending Scatter Plot
plt.figure(figsize=(9, 5.5))
ax = sns.scatterplot(
    data=df,
    x="Income",
    y="Total_Spending",
    hue="Segment",
    palette={"High Value Customer": "#10B981", "Budget Customer": "#3B82F6"},
    alpha=0.8,
    s=60,
    edgecolor="w"
)
plt.title("Customer Segments: Annual Income vs. Total Spending", fontsize=14, fontweight="bold", pad=12)
plt.xlabel("Annual Income (₹ / $)", fontsize=11, fontweight="bold")
plt.ylabel("Total Spending (₹ / $)", fontsize=11, fontweight="bold")
plt.legend(title="Customer Persona", frameon=True, facecolor="white", edgecolor="none")
plt.tight_layout()
plt.savefig("images/cluster_distribution.png", dpi=300)
plt.close()

# 2. 2D PCA Cluster Projection
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(9, 5.5))
plt.scatter(
    X_pca[clusters == 0, 0], X_pca[clusters == 0, 1],
    c="#10B981", label="High Value Customer", alpha=0.7, s=50, edgecolors="none"
)
plt.scatter(
    X_pca[clusters == 1, 0], X_pca[clusters == 1, 1],
    c="#3B82F6", label="Budget Customer", alpha=0.7, s=50, edgecolors="none"
)

# Plot Centroids
centroids_pca = pca.transform(model.cluster_centers_)
plt.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1],
    s=250, c="red", marker="X", label="Cluster Centroids", edgecolor="black", linewidth=1.5
)

plt.title("2D PCA Projection of Customer Clusters", fontsize=14, fontweight="bold", pad=12)
plt.xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)", fontsize=11, fontweight="bold")
plt.ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)", fontsize=11, fontweight="bold")
plt.legend(frameon=True, facecolor="white")
plt.tight_layout()
plt.savefig("images/pca_clusters.png", dpi=300)
plt.close()

print("Cluster plots generated successfully in images/")
