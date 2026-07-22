import os
import sys

import pandas as pd

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from src.exception import CustomerException
from src.logger import logging
from src.utils.main_utils import MainUtils


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig = DataValidationConfig()
    ):

        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.utils = MainUtils()

    def validate_dataset_schema(self) -> bool:

        try:

            validation_status = True

            train_df = pd.read_csv(
                self.data_ingestion_artifact.trained_file_path
            )

            test_df = pd.read_csv(
                self.data_ingestion_artifact.test_file_path
            )

            schema = self.utils.read_schema_config_file()

            required_columns = list(schema["columns"].keys())

            report = []

            # ===================================================
            # Empty Dataset Check
            # ===================================================

            if train_df.empty:
                validation_status = False
                report.append("Train dataset is empty")

            if test_df.empty:
                validation_status = False
                report.append("Test dataset is empty")

            # ===================================================
            # Required Column Check
            # ===================================================

            for column in required_columns:

                if column not in train_df.columns:
                    validation_status = False
                    report.append(f"Missing column in train data: {column}")

                if column not in test_df.columns:
                    validation_status = False
                    report.append(f"Missing column in test data: {column}")

            # ===================================================
            # Missing Value Check
            # ===================================================

            if train_df.isnull().sum().sum() > 0:
                validation_status = False
                report.append("Missing values found in train data")

            if test_df.isnull().sum().sum() > 0:
                validation_status = False
                report.append("Missing values found in test data")

            # ===================================================
            # Duplicate Row Check
            # ===================================================

            if train_df.duplicated().sum() > 0:
                validation_status = False
                report.append("Duplicate rows found in train data")

            if test_df.duplicated().sum() > 0:
                validation_status = False
                report.append("Duplicate rows found in test data")

            # ===================================================
            # Target Column Check
            # ===================================================

            if "Response" not in train_df.columns:
                validation_status = False
                report.append("Target column 'Response' missing in train data")

            if "Response" not in test_df.columns:
                validation_status = False
                report.append("Target column 'Response' missing in test data")

            # ===================================================
            # Save Validation Report
            # ===================================================

            os.makedirs(
                os.path.dirname(
                    self.data_validation_config.validation_report_file_path
                ),
                exist_ok=True
            )

            with open(
                self.data_validation_config.validation_report_file_path,
                "w"
            ) as file:

                file.write(f"Validation Status : {validation_status}\n\n")

                if validation_status:
                    file.write("All validation checks passed.\n")

                else:
                    for message in report:
                        file.write(message + "\n")

            logging.info(
                f"Validation report saved at "
                f"{self.data_validation_config.validation_report_file_path}"
            )

            return validation_status

        except Exception as e:
            raise CustomerException(e, sys)

    def initiate_data_validation(
        self,
    ) -> DataValidationArtifact:

        try:

            logging.info("Starting Data Validation Component")

            validation_status = self.validate_dataset_schema()

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path
            )

            logging.info(
                f"Data Validation Artifact : {data_validation_artifact}"
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomerException(e, sys)


# ==========================================================
# Run Data Validation
# ==========================================================

if __name__ == "__main__":

    from src.components.data_ingestion import DataIngestion

    try:

        print("=" * 50)
        print("Starting Data Validation Pipeline...")
        print("=" * 50)

        data_ingestion = DataIngestion()

        ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation = DataValidation(
            data_ingestion_artifact=ingestion_artifact
        )

        validation_artifact = (
            data_validation.initiate_data_validation()
        )

        print("\n✅ Data Validation Completed Successfully!")
        print(validation_artifact)

    except Exception as e:

        print("\n❌ Data Validation Failed!")
        print(e)