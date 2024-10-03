import os
import sys
import dill

from src.exception import CustomException
from src.logger import logging


def save_object(file_path,obj):
    try:
        logging.info("Save object function is started")
        dir_name = os.path.dirname(file_path)

        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("object saved")

    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path):
    try:
        logging.info("Load object function is started")

        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
        logging.info("object loaded")

    except Exception as e:
        raise CustomException(e,sys)