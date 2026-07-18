import os
import sys
from typing import Tuple

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.constant.database import COLLECTION_NAME
from src.data_access.customer_data import CustomerData
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomerException
from src.logger import logging
from src.utils.main_utils import MainUtils


class DataIngestion:

    def __init__(
            self,
            data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):

        self.data_ingestion_config = data_ingestion_config
        self.utils = MainUtils()

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Read data from MongoDB and save a copy into Feature Store.
        """

        try:

            logging.info("Starting data export from MongoDB")

            customer_data = CustomerData()

            dataframe = customer_data.export_collection_as_dataframe(
                collection_name=COLLECTION_NAME
            )

            logging.info(f"Dataframe Shape : {dataframe.shape}")

            feature_store_path = self.data_ingestion_config.feature_store_file_path

            os.makedirs(
                os.path.dirname(feature_store_path),
                exist_ok=True
            )

            dataframe.to_csv(
                feature_store_path,
                index=False,
                header=True
            )

            logging.info(
                f"Feature Store Created at {feature_store_path}"
            )

            return dataframe

        except Exception as e:
            raise CustomerException(e, sys)

    def split_data_as_train_test(
            self,
            dataframe: DataFrame
    ) -> Tuple[DataFrame, DataFrame]:

        try:

            logging.info("Performing Train-Test Split")

            train_df, test_df = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            ingested_dir = self.data_ingestion_config.ingested_data_dir

            os.makedirs(
                ingested_dir,
                exist_ok=True
            )

            train_df.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_df.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info("Train and Test files saved successfully")

            return train_df, test_df

        except Exception as e:
            raise CustomerException(e, sys)

    def initiate_data_ingestion(
            self
    ) -> DataIngestionArtifact:

        logging.info("Entered Data Ingestion Component")

        try:

            dataframe = self.export_data_into_feature_store()

            schema = self.utils.read_schema_config_file()

            if "drop_columns" in schema:
                dataframe = dataframe.drop(
                    schema["drop_columns"],
                    axis=1
                )

            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(
                f"Data Ingestion Artifact : {data_ingestion_artifact}"
            )

            logging.info("Data Ingestion Completed Successfully")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomerException(e, sys)