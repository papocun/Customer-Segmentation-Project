import os
import sys
import yaml
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact
)

from src.exception import CustomerException
from src.logger import logging

from src.file_utils import (
    save_object,
    save_numpy_array_data
)


class DataTransformation:

    def __init__(
            self,
            data_ingestion_artifact: DataIngestionArtifact,
            data_validation_artifact: DataValidationArtifact,
            data_transformation_config: DataTransformationConfig = DataTransformationConfig()
    ):

        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path):

        try:

            return pd.read_csv(file_path)

        except Exception as e:

            raise CustomerException(e, sys)

    @staticmethod
    def read_schema():

        try:

            with open("config/schema.yaml", "r") as file:

                schema = yaml.safe_load(file)

            return schema

        except Exception as e:

            raise CustomerException(e, sys)

    def get_data_transformer_object(self):

        try:

            schema = self.read_schema()

            numerical_columns = schema["numerical_columns"]
            categorical_columns = schema["categorical_columns"]

            logging.info("Creating preprocessing pipelines")

            numerical_pipeline = Pipeline(

                steps=[

                    (
                        "scaler",
                        StandardScaler()
                    )

                ]

            )

            categorical_pipeline = Pipeline(

                steps=[

                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore"
                        )
                    )

                ]

            )

            preprocessor = ColumnTransformer(

                transformers=[

                    (
                        "numerical_pipeline",
                        numerical_pipeline,
                        numerical_columns
                    ),

                    (
                        "categorical_pipeline",
                        categorical_pipeline,
                        categorical_columns
                    )

                ]

            )

            return preprocessor

        except Exception as e:

            raise CustomerException(e, sys)

    def initiate_data_transformation(self):

        try:

            if not self.data_validation_artifact.validation_status:

                raise Exception("Data Validation Failed")

            logging.info("Reading Train & Test Files")

            train_df = self.read_data(
                self.data_ingestion_artifact.trained_file_path
            )

            test_df = self.read_data(
                self.data_ingestion_artifact.test_file_path
            )

            schema = self.read_schema()

            target_column = schema["target_column"]

            drop_columns = schema.get(
                "drop_columns",
                []
            )

            train_df = train_df.drop(
                columns=drop_columns,
                errors="ignore"
            )

            test_df = test_df.drop(
                columns=drop_columns,
                errors="ignore"
            )

            X_train = train_df.drop(
                columns=[target_column],
                axis=1
            )

            y_train = train_df[target_column]

            X_test = test_df.drop(
                columns=[target_column],
                axis=1
            )

            y_test = test_df[target_column]

            logging.info("Creating Preprocessor")

            preprocessor = self.get_data_transformer_object()

            logging.info("Fitting Preprocessor")

            X_train = preprocessor.fit_transform(X_train)

            X_test = preprocessor.transform(X_test)

            train_arr = np.c_[

                X_train,

                np.array(y_train)

            ]

            test_arr = np.c_[

                X_test,

                np.array(y_test)

            ]
            
            logging.info("Saving transformed numpy arrays")

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                test_arr
            )

            logging.info("Saving fitted preprocessor object")

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor
            )

            logging.info("Data Transformation completed successfully")

            data_transformation_artifact = DataTransformationArtifact(

                transformed_train_file_path=
                self.data_transformation_config.transformed_train_file_path,

                transformed_test_file_path=
                self.data_transformation_config.transformed_test_file_path,

                transformed_object_file_path=
                self.data_transformation_config.transformed_object_file_path

            )

            return data_transformation_artifact

        except Exception as e:

            raise CustomerException(e, sys)


if __name__ == "__main__":

    from src.components.data_ingestion import DataIngestion
    from src.components.data_validation import DataValidation

    logging.info("Starting Data Ingestion")

    data_ingestion = DataIngestion()

    ingestion_artifact = data_ingestion.initiate_data_ingestion()

    logging.info("Starting Data Validation")

    data_validation = DataValidation(
        data_ingestion_artifact=ingestion_artifact
    )

    validation_artifact = data_validation.initiate_data_validation()

    logging.info("Starting Data Transformation")

    data_transformation = DataTransformation(
        data_ingestion_artifact=ingestion_artifact,
        data_validation_artifact=validation_artifact
    )

    transformation_artifact = (
        data_transformation.initiate_data_transformation()
    )

    print("\nData Transformation Completed Successfully\n")

    print(transformation_artifact)