import sys
import pandas as pd

from src.config.configuration import MongoDBClient
from src.exception import CustomerException


class CustomerData:

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient()
        except Exception as e:
            raise CustomerException(e, sys)

    def export_collection_as_dataframe(self, collection_name):

        try:
            collection = self.mongo_client.database[collection_name]

            dataframe = pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns:
                dataframe.drop("_id", axis=1, inplace=True)

            return dataframe

        except Exception as e:
            raise CustomerException(e, sys)