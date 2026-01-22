from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
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


    except Exception as e:
        raise NetworkSecurityException(e,sys)
