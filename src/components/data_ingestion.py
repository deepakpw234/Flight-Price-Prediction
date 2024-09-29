import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException


@dataclass
class DataIngestionConfig:
    train_data = os.path.join("artifacts","train_data.csv")
    test_data = os.path.join("artifacts","test_data.csv")
    raw_data = os.path.join("artifacts","raw_data.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

        os.makedirs((os.path.join(os.getcwd(),"artifacts")),exist_ok=True)


    def initiate_data_ingestion(self):
        try:
            logging.info("Data ingestion started")

            df = pd.read_csv(r"notebook\flight data.csv")
            logging.info("raw data is loaded into dataframe")

            train_data, test_data = train_test_split(df,test_size = 0.2, random_state = 42)
            logging.info("Train test split done")

            df.to_csv(self.data_ingestion_config.raw_data,index=False,header=True)
            logging.info("raw data saved to csv in artifacts directory")

            train_data.to_csv(self.data_ingestion_config.train_data,index=False,header=True)
            logging.info("Train data is saved into csv and ready for cleaning")

            test_data.to_csv(self.data_ingestion_config.test_data,index=False,header=True)
            logging.info("Test data is saved into csv and ready for cleaning")

            return (
                self.data_ingestion_config.raw_data,
                self.data_ingestion_config.train_data,
                self.data_ingestion_config.test_data
            )

        except Exception as e:
            raise CustomException(e,sys)
        

