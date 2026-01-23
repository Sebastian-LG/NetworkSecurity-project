from network_security.entity.artifact_entity  import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os,sys



class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        
        try:

            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # Use inside the class, we don't need to instantiate the class
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns is {number_of_columns}")
            logging.info(f"Dataframe has {len(dataframe)} columns")
            
            if len(dataframe) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({column:{"p_value":float(is_same_dist.pvalue),
                                       "drift_status":is_found} })
                
            drif_report_file_path = self.data_validation_config.data_drift_report_file_path
            dir_path = os.path.dirname(drif_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(file_path=drif_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            # Validate number of columns
            status = self.validate_number_columns(train_df)
            if not status:
                error_message = f"Train dataframe doesn't have all columns"
            
            status = self.validate_number_columns(test_df)
            if not status:
                error_message = f"Test dataframe doesn't have all columns"
            
            # Other validations
            # Check numerical columns

            # Let's check data drift
            status = self.detect_dataset_drift(train_df,test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,
                            header=True,index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,
                            header=True,index=False)
            
            data_validation_artifact = DataValidationArtifact(validation_status = status,
            valid_train_file_path = self.data_validation_config.valid_train_file_path,
            valid_test_file_path = self.data_validation_config.valid_test_file_path,
            invalid_train_file_path = self.data_validation_config.invalid_train_file_path,
            invalid_test_file_path = self.data_validation_config.invalid_test_file_path,
            drift_report_file_path = self.data_validation_config.data_drift_report_file_path)

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)