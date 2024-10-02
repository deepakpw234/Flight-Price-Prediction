from src.components.data_ingestion import DataIngestion
from src.components.data_cleaning import DataCleaning
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



if __name__ == "__main__":
    a = DataIngestion()
    _,train_data_path,test_data_path = a.initiate_data_ingestion()
    
    b = DataCleaning()
    flight,flight_test=b.get_data_clean(train_data_path,test_data_path)

    f = DataTransformation()
    train_arr,test_arr,path = f.initiate_data_transformation(flight,flight_test)

    m = ModelTrainer()
    m.intiate_model_training(train_arr,test_arr)