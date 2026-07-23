"""K-Means model-training component for customer segmentation."""

import json
import os
import sys

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

from src.entity.artifact_entity import DataTransformationArtifact
from src.entity.config_entity import (
    ClusteringMetricArtifact,
    ModelTrainerArtifact,
    ModelTrainerConfig,
)
from src.exception import CustomerException
from src.file_utils import save_object
from src.logger import logging


class ModelTrainer:
    """Select and fit a K-Means model using transformed customer features."""

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(),
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    @staticmethod
    def _load_features(file_path: str) -> np.ndarray:
        """Load features, excluding the final ``Response`` target column.

        The target is useful for campaign-response analysis, but must not be
        used to create unsupervised customer segments.
        """
        array = np.load(file_path)
        if array.ndim != 2 or array.shape[1] < 2:
            raise ValueError(
                "Expected a 2D transformed array containing features and a target column."
            )
        return array[:, :-1]

    def _select_best_k(self, X_train: np.ndarray) -> tuple:
        """Return the k with the largest silhouette score (notebook approach)."""
        upper_k = min(self.model_trainer_config.max_clusters, len(X_train) - 1)
        if upper_k < self.model_trainer_config.min_clusters:
            raise ValueError("Not enough training samples to fit K-Means.")

        best_k = None
        best_score = -np.inf
        candidate_scores = {}

        for k in range(self.model_trainer_config.min_clusters, upper_k + 1):
            candidate = KMeans(
                n_clusters=k,
                n_init=self.model_trainer_config.n_init,
                random_state=self.model_trainer_config.random_state,
            )
            labels = candidate.fit_predict(X_train)
            score = float(silhouette_score(X_train, labels))
            candidate_scores[k] = score
            logging.info("K-Means candidate k=%s, silhouette=%.4f", k, score)

            if score > best_score:
                best_k = k
                best_score = score

        return best_k, candidate_scores

    @staticmethod
    def _calculate_metrics(X: np.ndarray, labels: np.ndarray) -> ClusteringMetricArtifact:
        return ClusteringMetricArtifact(
            silhouette_score=float(silhouette_score(X, labels)),
            davies_bouldin_score=float(davies_bouldin_score(X, labels)),
            calinski_harabasz_score=float(calinski_harabasz_score(X, labels)),
        )

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """Train K-Means on train data and evaluate the selected model on test data."""
        try:
            logging.info("Starting K-Means model training")
            X_train = self._load_features(
                self.data_transformation_artifact.transformed_train_file_path
            )
            X_test = self._load_features(
                self.data_transformation_artifact.transformed_test_file_path
            )

            best_k, candidate_scores = self._select_best_k(X_train)
            model = KMeans(
                n_clusters=best_k,
                n_init=self.model_trainer_config.n_init,
                random_state=self.model_trainer_config.random_state,
            )
            model.fit(X_train)

            # Hold-out data is never used while fitting or choosing k.
            test_labels = model.predict(X_test)
            metric_artifact = self._calculate_metrics(X_test, test_labels)

            save_object(self.model_trainer_config.trained_model_file_path, model)
            os.makedirs(
                os.path.dirname(self.model_trainer_config.metrics_file_path),
                exist_ok=True,
            )
            with open(self.model_trainer_config.metrics_file_path, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "best_k": best_k,
                        "selection_metric": "silhouette_score",
                        "candidate_train_silhouette_scores": candidate_scores,
                        "test_metrics": metric_artifact.__dict__,
                    },
                    file,
                    indent=2,
                )

            logging.info(
                "K-Means training complete: best_k=%s, test silhouette=%.4f",
                best_k,
                metric_artifact.silhouette_score,
            )
            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                best_k=best_k,
                metric_artifact=metric_artifact,
            )
        except Exception as e:
            raise CustomerException(e, sys)
