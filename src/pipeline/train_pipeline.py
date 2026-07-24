"""Training pipeline for Customer Segmentation."""

import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.exception import CustomerException
from src.logger import logging


class TrainPipeline:
    """Orchestrates the end-to-end training workflow."""

    def __init__(self):
        pass

    def run_pipeline(self):
        """
        Executes the complete ML training pipeline.

        Flow:
        Data Ingestion
            ↓
        Data Validation
            ↓
        Data Transformation
            ↓
        Model Training
        """

        try:
            logging.info("=" * 60)
            logging.info("Starting Customer Segmentation Training Pipeline")
            logging.info("=" * 60)

            # ==========================================================
            # Data Ingestion
            # ==========================================================
            logging.info("Starting Data Ingestion...")

            data_ingestion = DataIngestion()

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info("Data Ingestion Completed Successfully.")

            # ==========================================================
            # Data Validation
            # ==========================================================
            logging.info("Starting Data Validation...")

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )

            logging.info("Data Validation Completed Successfully.")

            # ==========================================================
            # Data Transformation
            # ==========================================================
            logging.info("Starting Data Transformation...")

            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info("Data Transformation Completed Successfully.")

            # ==========================================================
            # Model Trainer
            # ==========================================================
            logging.info("Starting Model Training...")

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact
            )

            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )

            logging.info("Model Training Completed Successfully.")

            logging.info("=" * 60)
            logging.info("Training Pipeline Executed Successfully.")
            logging.info("=" * 60)

            return model_trainer_artifact

        except Exception as e:
            logging.exception(e)
            raise CustomerException(e, sys) from e