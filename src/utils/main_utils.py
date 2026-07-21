import sys
import yaml

from src.exception import CustomerException
from src.constant.training_pipeline import SCHEMA_FILE_PATH


class MainUtils:

    def read_yaml_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                return yaml.safe_load(file)

        except Exception as e:
            raise CustomerException(e, sys)

    def read_schema_config_file(self):
        return self.read_yaml_file(SCHEMA_FILE_PATH)