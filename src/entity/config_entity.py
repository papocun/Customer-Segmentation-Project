from dataclasses import dataclass
import os


@dataclass
class DataIngestionConfig:

    artifact_dir: str = "artifacts"

    feature_store_file_path: str = os.path.join(
        artifact_dir,
        "feature_store",
        "customer_data.csv"
    )

    ingested_data_dir: str = os.path.join(
        artifact_dir,
        "ingested_data"
    )

    training_file_path: str = os.path.join(
        ingested_data_dir,
        "train.csv"
    )

    testing_file_path: str = os.path.join(
        ingested_data_dir,
        "test.csv"
    )

    train_test_split_ratio: float = 0.2




@dataclass
class DataValidationConfig:

    artifact_dir: str = "artifacts"

    validation_report_file_path: str = os.path.join(
        artifact_dir,
        "data_validation",
        "status.txt"
    )


@dataclass
class DataTransformationConfig:

    artifact_dir = "artifacts"

    transformed_train_file_path = os.path.join(
        artifact_dir,
        "data_transformation",
        "train.npy"
    )

    transformed_test_file_path = os.path.join(
        artifact_dir,
        "data_transformation",
        "test.npy"
    )

    transformed_object_file_path = os.path.join(
        artifact_dir,
        "data_transformation",
        "preprocessor.pkl"
    )


@dataclass
class ModelTrainerConfig:
    artifact_dir: str = "artifacts"
    trained_model_file_path: str = os.path.join(
        artifact_dir, "model_trainer", "kmeans_model.pkl"
    )
    metrics_file_path: str = os.path.join(
        artifact_dir, "model_trainer", "clustering_metrics.json"
    )
    min_clusters: int = 2
    max_clusters: int = 8
    random_state: int = 42
    n_init: int = 25

@dataclass
class ClusteringMetricArtifact:
    silhouette_score: float
    davies_bouldin_score: float
    calinski_harabasz_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    best_k: int
    metric_artifact: ClusteringMetricArtifact
