"""
K-Means Model Trainer
"""

import json
import os
import sys

import numpy as np

from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)

from src.entity.artifact_entity import (
    DataTransformationArtifact
)

from src.entity.config_entity import (
    ModelTrainerConfig,
    ModelTrainerArtifact,
    ClusteringMetricArtifact
)

from src.file_utils import save_object
from src.exception import CustomerException
from src.logger import logging


class ModelTrainer:

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig = ModelTrainerConfig()
    ):

        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    @staticmethod
    def _load_features(file_path: str):

        try:

            logging.info(f"Loading transformed data : {file_path}")

            array = np.load(file_path)

            if array.ndim != 2:

                raise ValueError(
                    "Expected 2D transformed array."
                )

            if array.shape[1] < 2:

                raise ValueError(
                    "Expected transformed features with Response column."
                )

            X = array[:, :-1]

            return X

        except Exception as e:

            raise CustomerException(e, sys)

    def _select_best_k(self, X_train):

        try:

            upper_k = min(

                self.model_trainer_config.max_clusters,

                len(X_train) - 1

            )

            if upper_k < self.model_trainer_config.min_clusters:

                raise ValueError(
                    "Insufficient samples for clustering."
                )

            best_k = None

            best_score = -1

            scores = {}

            logging.info("Selecting optimal number of clusters")

            for k in range(

                self.model_trainer_config.min_clusters,

                upper_k + 1

            ):

                model = KMeans(

                    n_clusters=k,

                    random_state=self.model_trainer_config.random_state,

                    n_init=self.model_trainer_config.n_init

                )

                labels = model.fit_predict(X_train)

                score = silhouette_score(
                    X_train,
                    labels
                )

                scores[k] = float(score)

                logging.info(
                    f"k={k}  Silhouette={score:.4f}"
                )

                if score > best_score:

                    best_score = score

                    best_k = k

            logging.info(f"Best K Selected : {best_k}")

            return best_k, scores

        except Exception as e:

            raise CustomerException(e, sys)

    @staticmethod
    def _calculate_metrics(X, labels):

        return ClusteringMetricArtifact(

            silhouette_score=float(

                silhouette_score(X, labels)

            ),

            davies_bouldin_score=float(

                davies_bouldin_score(X, labels)

            ),

            calinski_harabasz_score=float(

                calinski_harabasz_score(X, labels)

            )

        )

    def initiate_model_trainer(self):

        try:

            logging.info("Starting Model Training")

            X_train = self._load_features(

                self.data_transformation_artifact.transformed_train_file_path

            )

            X_test = self._load_features(

                self.data_transformation_artifact.transformed_test_file_path

            )

            best_k, candidate_scores = self._select_best_k(

                X_train

            )

            logging.info("Training Final KMeans Model")

            model = KMeans(

                n_clusters=best_k,

                random_state=self.model_trainer_config.random_state,

                n_init=self.model_trainer_config.n_init

            )

            model.fit(X_train)

            test_labels = model.predict(

                X_test

            )

            metric_artifact = self._calculate_metrics(

                X_test,

                test_labels

            )

            logging.info("Saving trained model")

            save_object(

                self.model_trainer_config.trained_model_file_path,

                model

            )

            metadata = {

                "best_k": best_k,

                "selection_metric": "silhouette_score",

                "candidate_train_silhouette_scores": candidate_scores,

                "cluster_centers": model.cluster_centers_.tolist(),

                "test_metrics": {

                    "silhouette_score": metric_artifact.silhouette_score,

                    "davies_bouldin_score": metric_artifact.davies_bouldin_score,

                    "calinski_harabasz_score": metric_artifact.calinski_harabasz_score

                }

            }

            os.makedirs(

                os.path.dirname(

                    self.model_trainer_config.metrics_file_path

                ),

                exist_ok=True

            )

            with open(

                self.model_trainer_config.metrics_file_path,

                "w",

                encoding="utf-8"

            ) as file:

                json.dump(

                    metadata,

                    file,

                    indent=4

                )

            logging.info(

                f"KMeans Model Training Completed | Best K = {best_k}"

            )

            return ModelTrainerArtifact(

                trained_model_file_path=self.model_trainer_config.trained_model_file_path,

                best_k=best_k,

                metric_artifact=metric_artifact

            )

        except Exception as e:

            raise CustomerException(e, sys)