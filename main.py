from src.components.data_ingestion import DataIngestion
from src.components.data_cleaning import DataCleaning
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



if __name__ == "__main__":
    data_inges = DataIngestion()
    _,train_data_path,test_data_path = data_inges.initiate_data_ingestion()
    
    data_clean = DataCleaning()
    flight,flight_test=data_clean.get_data_clean(train_data_path,test_data_path)

    data_trans = DataTransformation()
    train_arr,test_arr,path = data_trans.initiate_data_transformation(flight,flight_test)

    model_train = ModelTrainer()
    model_train.intiate_model_training(train_arr,test_arr)