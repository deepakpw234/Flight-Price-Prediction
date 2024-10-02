import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass


from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformation(self):
        try:
            logging.info("Data Transforamtion Started")

            num_column = ['Total_Stops', 'Day', 'Month', 'Year', 
                          'Dep_hour', 'Dep_min', 'Arrival_hour', 'Arrival_min', 
                          'duration_hours', 'duration_minutes', 'duration']
            cat_column = ['Airline', 'Source', 'Destination']
            

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ('scaler',StandardScaler())
                ]
            )
            logging.info("numerical pipeline has been created")

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one hot encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("categorical pipeline has been created")


            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_column),
                    ("cat_pipeline",cat_pipeline,cat_column)
                ]
            )
            logging.info("columnTransformer created")

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,flight, flight_test):
        try:

            target_feature = "Price"
            X_train = flight.drop(columns=[target_feature],axis=1)
            X_test = flight_test.drop(columns=[target_feature],axis=1)

            y_train = flight[target_feature]
            y_test = flight_test[target_feature]
            logging.info("X and Y train test split done")

            preprocessor_obj = self.get_data_transformation()
            logging.info("Preprocessor is working fine")

            X_train_arr = preprocessor_obj.fit_transform(X_train)
            X_test_arr = preprocessor_obj.transform(X_test)
            logging.info("fit and transform is completed")

            train_arr = np.c_[
                X_train_arr, np.array(y_train)
            ]

            test_arr = np.c_[
                X_test_arr, np.array(y_test)
            ]
        
            
            save_object(
                self.data_transformation_config.preprocessor_path,
                preprocessor_obj
            )
            logging.info("Processor save in the pickle file")

            return (
                train_arr,test_arr,self.data_transformation_config.preprocessor_path
            )


        except Exception as e:
            raise CustomException(e,sys)


