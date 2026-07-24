import os
import sys
import pickle
import numpy as np

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomerException


def save_object(file_path, obj):
    """
    Save any Python object as a pickle file.
    """

    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomerException(e, sys)


def load_object(file_path):
    """
    Load a pickled object.
    """

    try:

        with open(file_path, "rb") as file_obj:

            return pickle.load(file_obj)

    except Exception as e:

        raise CustomerException(e, sys)


def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    Save numpy array.
    """

    try:

        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:

            np.save(file_obj, array)

    except Exception as e:

        raise CustomerException(e, sys)


def evaluate_models(
    X_train,
    y_train,
    X_test,
    y_test,
    models,
    param
):
    """
    Evaluate regression models using GridSearchCV.
    """

    try:

        report = {}

        for model_name, model in models.items():

            para = param[model_name]

            gs = GridSearchCV(
                estimator=model,
                param_grid=para,
                cv=3
            )

            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_score = r2_score(y_train, y_train_pred)

            test_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_score

        return report

    except Exception as e:

        raise CustomerException(e, sys)