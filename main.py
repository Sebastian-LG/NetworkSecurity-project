from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        logging.info("Enter try block")
        training_pl_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pl_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config_obj)

        logging.info("Initiate data ingestion")
        data_ingestion_artifact = data_ingestion_obj.initiate_data_ingestion()
        print(data_ingestion_artifact)

        logging.info("Initiate data validation")
        data_validation_config = DataValidationConfig(training_pl_obj)
        data_validation_obj = DataValidation(data_ingestion_artifact,data_validation_config)
        
        data_validation_artifact = data_validation_obj.initiate_data_validation()

    except Exception as e:
        raise NetworkSecurityException(e,sys)
