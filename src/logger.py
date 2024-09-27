import os
import logging
from datetime import datetime
from pathlib import Path

log_file_name = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
dir_path = os.path.join(os.getcwd(),"log")
os.makedirs(dir_path,exist_ok=True)

log_file_path = os.path.join(dir_path,log_file_name)


logging.basicConfig(
    filename=log_file_path,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

