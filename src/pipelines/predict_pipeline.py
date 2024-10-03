import os
import sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging


from src.utils import load_object


class PredictPipeline:
    def __init__(self) -> None:
        pass

    def predict_price(self,df):
        try:
            preprocessor_path = os.path.join("artifacts","preprocessor.pkl")
            model_path = os.path.join("artifacts","model.pkl")
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            scaled_data = preprocessor.transform(df)
            pred = model.predict(scaled_data)
            
            return pred


        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,Airline: str, Source: str, Destination: str, Total_Stops: int,
            Day: int, Month: int, Year:int, Dep_hour: int,Dep_min: int, Arrival_hour: int, 
            Arrival_min: int, duration_hours: int, duration_minutes: int, duration: int):
        self.Airline = Airline
        self.Source = Source
        self.Destination = Destination
        self.Total_Stops = Total_Stops
        self.Day = Day
        self.Month = Month
        self.Year = Year
        self.Dep_hour = Dep_hour
        self.Dep_min = Dep_min
        self.Arrival_hour = Arrival_hour
        self.Arrival_min = Arrival_min
        self.duration_hours = duration_hours
        self.duration_minutes = duration_minutes
        self.duration = duration


    def get_data_as_frame(self):
        try:
            custom_dataframe = {
                'Airline' : [self.Airline],
                'Source' : [self.Source],
                'Destination' : [self.Destination],
                'Total_Stops' : [self.Total_Stops],
                'Day' : [self.Day],
                'Month' : [self.Month],
                'Year' : [self.Year],
                'Dep_hour' : [self.Dep_hour],
                'Dep_min' : [self.Dep_min],
                'Arrival_hour' : [self.Arrival_hour],
                'Arrival_min' : [self.Arrival_min],
                'duration_hours' : [self.duration_hours],
                'duration_minutes' : [self.duration_minutes],
                'duration' : [self.duration]
            }

            df = pd.DataFrame(custom_dataframe)
            print(df)

            return df
        
        except Exception as e:
            raise CustomException(e,sys)
        


