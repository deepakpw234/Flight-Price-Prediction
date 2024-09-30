import os
import sys
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException

from dataclasses import dataclass

@dataclass
class DataCleaningConfig:
    train_cleaned = os.path.join('artifacts','train_cleaned.csv')
    test_cleaned = os.path.join('artifacts','test_cleaned.csv')


class DataCleaning:
    def __init__(self):
        self.data_config = DataCleaningConfig()
        print(self.data_config.train_cleaned)

    def get_data_clean(self,train_data_path,test_data_path):
        try:
            logging.info("Data Cleaning Started")
            flight = pd.read_csv(train_data_path)
            
            
            # Drpping the na value
            flight = flight.dropna()
            logging.info("na value dropped")

            # Changing the date of journey column into date format
            flight['Date_of_Journey'] = pd.to_datetime(flight['Date_of_Journey'],format="%d/%m/%Y",dayfirst=True)
            flight["Day"] = flight['Date_of_Journey'].dt.day
            flight['Month'] = flight['Date_of_Journey'].dt.month
            flight['Year'] = flight['Date_of_Journey'].dt.year
            flight = flight.drop(['Date_of_Journey'],axis=1)
            logging.info("Changed the date of journey column into date format and split in day,month and year")

            # Converting departure time into hours and minutes
            flight['Dep_Time'] = pd.to_datetime(flight['Dep_Time'],format="%H:%M")
            flight['Dep_hour'] = flight['Dep_Time'].dt.hour
            flight['Dep_min'] = flight['Dep_Time'].dt.minute
            flight = flight.drop(['Dep_Time'],axis=1)
            logging.info("Changed the departure time column into date format and split in hours and minutes")

            # Converting arrival time into hours and minutes
            flight['Arrival_Time'] = pd.to_datetime(flight['Arrival_Time'])
            flight['Arrival_hour'] = flight['Arrival_Time'].dt.hour
            flight['Arrival_min'] = flight['Arrival_Time'].dt.minute
            flight = flight.drop('Arrival_Time',axis=1)
            logging.info("Changed the arrival time column into date format and split in hours and minutes")

            # Converting duration time into hours and minutes
            duration_list = list(flight['Duration'])
            for i in range(len(duration_list)):
                if len(duration_list[i].split()) != 2:
                    if "h" in duration_list[i]:
                        duration_list[i] = duration_list[i] + " 0m"
                    else:
                        duration_list[i] = "0h " + duration_list[i]

                    
            duration_hours = []        
            duration_minutes = []
            for i in range(len(duration_list)):
                duration_hours.append(int(duration_list[i].split("h")[0]))
                duration_minutes.append(int((duration_list[i].split()[1]).replace("m","")))

            flight['duration_hours'] = duration_hours
            flight['duration_minutes'] = duration_minutes
            flight = flight.drop(['Duration'],axis=1)
            flight['duration']=flight['duration_hours']*60+flight['duration_minutes']
            logging.info("Changed duraton column into hours and minutes")

            flight = flight.drop(['Additional_Info','Route'],axis=1)
            flight = flight.replace({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4})



            # Test dataset loaded
            flight_test = pd.read_csv(test_data_path)
            logging.info("Test dataset loaded")


            # Changing the date of journey column into date format
            flight_test['Date_of_Journey'] = pd.to_datetime(flight_test['Date_of_Journey'], format="%d/%m/%Y",dayfirst=True)
            flight_test['Day'] = flight_test['Date_of_Journey'].dt.day
            flight_test['Month'] = flight_test['Date_of_Journey'].dt.month
            flight_test['Year'] = flight_test['Date_of_Journey'].dt.year
            flight_test = flight_test.drop('Date_of_Journey',axis=1)
            logging.info("Changed the date of journey column into date format and split in day,month and year")

            
            # Converting departure time into hours and minutes
            flight_test['Dep_hour'] = pd.to_datetime(flight_test['Dep_Time'],format="%H:%M").dt.hour
            flight_test['Dep_min'] = pd.to_datetime(flight_test['Dep_Time'],format="%H:%M").dt.minute
            logging.info("Changed the departure time column into date format and split in hours and minutes")


            # Converting arrival time into hours and minutes
            flight_test['Arrival_hour'] = pd.to_datetime(flight_test['Arrival_Time']).dt.hour
            flight_test['Arrival_min'] = pd.to_datetime(flight_test['Arrival_Time']).dt.minute
            flight_test = flight_test.drop(['Dep_Time','Arrival_Time'],axis=1)
            logging.info("Changed the arrival time column into date format and split in hours and minutes")


            # Converting duration time into hours and minutes
            duration_list_test = list(flight_test['Duration'])
            for i in range(len(duration_list_test)):
                if len(duration_list_test[i].split()) != 2:
                    if "h" in duration_list_test[i]:
                        duration_list_test[i] = duration_list_test[i] + " 0m"
                    else:
                        duration_list_test[i] = "0h " + duration_list_test[i]
        
                    
            duration_hours_test = []        
            duration_minutes_test = []
            for i in range(len(duration_list_test)):
                duration_hours_test.append(int(duration_list_test[i].split("h")[0]))
                duration_minutes_test.append(int((duration_list_test[i].split()[1]).replace("m","")))

            
            flight_test['duration_hours'] = duration_hours_test
            flight_test['duration_minutes'] = duration_minutes_test
            flight_test = flight_test.drop(['Route','Duration','Additional_Info'],axis=1)
            flight_test['duration'] = flight_test['duration_hours']*60+flight_test['duration_minutes']
            logging.info("Changed duraton column into hours and minutes")

            flight_test = flight_test.replace({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4})
            
            # print(flight)
            # print(flight_test)
            os.makedirs((os.path.join(os.getcwd(),"artifacts")),exist_ok=True)
            logging.info("Directory Created")

            flight.to_csv(self.data_config.train_cleaned,index=False,header=True)
            flight_test.to_csv(self.data_config.test_cleaned,index=False,header=True)
            logging.info("Cleaned data set saved to csv")

            return flight,flight_test
            

        except Exception as e:
            raise CustomException(e,sys)


