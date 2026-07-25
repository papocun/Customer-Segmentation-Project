import os

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.file_utils import load_object

# -----------------------------
# Load Data
# -----------------------------

df = pd.read_csv("data/processed/marketing_cleaned.csv")

model_features = [
    "Income",
    "Total_Spending",
    "Total_Purchases",
    "Recency",
    "NumWebVisitsMonth",
    "Total_Promo_Accepted",
    "Children"
]

# -----------------------------
# Load Preprocessor
# -----------------------------

preprocessor = load_object(
    "artifacts/data_transformation/preprocessor.pkl"
)

X = preprocessor.transform(df[model_features])

# -----------------------------
# Calculate Metrics
# -----------------------------

ks = range(2, 9)

inertia = []
silhouette_scores = []

for k in ks:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    inertia.append(model.inertia_)

    silhouette_scores.append(
        silhouette_score(X, labels)
    )

# -----------------------------
# Save Location
# -----------------------------

save_dir = "artifacts/model_trainer"

os.makedirs(save_dir, exist_ok=True)

# -----------------------------
# Elbow Curve
# -----------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    ks,
    inertia,
    marker="o",
    linewidth=2
)

best_k = 2

plt.scatter(
    best_k,
    inertia[best_k - 2],
    s=120,
    color="red",
    zorder=5
)

plt.annotate(
    f"Selected k = {best_k}",
    (best_k, inertia[best_k - 2]),
    xytext=(15, -15),
    textcoords="offset points",
    fontsize=10,
    color="red"
)

plt.title("Elbow Method")

plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")

plt.grid(True)

plt.savefig(
    os.path.join(save_dir, "elbow_curve.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# -----------------------------
# Silhouette Curve
# -----------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    ks,
    silhouette_scores,
    marker="o",
    linewidth=2
)

best_index = silhouette_scores.index(max(silhouette_scores))

plt.scatter(
    ks[best_index],
    silhouette_scores[best_index],
    s=100
)

plt.annotate(
    f"Best k = {ks[best_index]}",
    (
        ks[best_index],
        silhouette_scores[best_index]
    ),
    xytext=(5, 5),
    textcoords="offset points"
)

plt.title("Silhouette Score")

plt.xlabel("Number of Clusters (k)")

plt.ylabel("Silhouette Score")

plt.grid(True)

plt.savefig(
    os.path.join(
        save_dir,
        "silhouette_curve.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Analysis Completed Successfully!")