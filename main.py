from src.components.data_ingestion import DataIngestion
from src.components.data_cleaning import DataCleaning



if __name__ == "__main__":
    a = DataIngestion()
    a.initiate_data_ingestion()
    
    b = DataCleaning()
    b.get_data_clean()
