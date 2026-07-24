import os
import sys
import pandas as pd

from src.exception import CustomerException
from src.file_utils import load_object
from src.logger import logging


class PredictPipeline:
    """
    Prediction Pipeline

    Loads:
    1. Preprocessor
    2. Trained KMeans Model

    Returns:
    Cluster Prediction
    """

    def __init__(self):

        self.preprocessor_path = os.path.join(
            "artifacts",
            "data_transformation",
            "preprocessor.pkl"
        )

        self.model_path = os.path.join(
            "artifacts",
            "model_trainer",
            "kmeans_model.pkl"
        )

    def predict(self, features: pd.DataFrame):

        try:

            logging.info("Loading preprocessor object")

            preprocessor = load_object(
                self.preprocessor_path
            )

            logging.info("Loading trained KMeans model")

            model = load_object(
                self.model_path
            )

            logging.info("Transforming input features")

            transformed_features = preprocessor.transform(features)

            logging.info("Predicting customer segment")

            prediction = model.predict(transformed_features)

            return prediction

        except Exception as e:

            raise CustomerException(e, sys)


class CustomerData:
    """
    Customer Input Class
    """

    def __init__(

        self,

        Income,
        Total_Spending,
        Total_Purchases,
        Recency,
        NumWebVisitsMonth,
        Total_Promo_Accepted,
        Children

    ):

        self.Income = Income
        self.Total_Spending = Total_Spending
        self.Total_Purchases = Total_Purchases
        self.Recency = Recency
        self.NumWebVisitsMonth = NumWebVisitsMonth
        self.Total_Promo_Accepted = Total_Promo_Accepted
        self.Children = Children

    def get_data_as_dataframe(self):

        try:

            custom_data_input = {

                "Income": [self.Income],

                "Total_Spending": [self.Total_Spending],

                "Total_Purchases": [self.Total_Purchases],

                "Recency": [self.Recency],

                "NumWebVisitsMonth": [self.NumWebVisitsMonth],

                "Total_Promo_Accepted": [self.Total_Promo_Accepted],

                "Children": [self.Children]

            }

            return pd.DataFrame(custom_data_input)

        except Exception as e:

            raise CustomerException(e, sys)