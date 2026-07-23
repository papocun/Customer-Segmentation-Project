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