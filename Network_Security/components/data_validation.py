from Network_Security.logging.logger import logging
from Network_Security.constant import SCHEMA_FILE_PATH
from Network_Security.utils import read_yaml_file, write_yaml_file
from Network_Security.entity.artifact import Data_Ingestion_Artifact, Data_validation_Artifact
from Network_Security.entity.config import Data_validation_config
from Network_Security.exception.exception import NetworkSecurityException
from evidently import Report
from evidently.presets import DataDriftPreset
import pandas as pd
import json
import sys


class Data_validation:
    def __init__(self, data_ingestion_artifact: Data_Ingestion_Artifact,
                data_validation_config: Data_validation_config):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_yaml = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            if self._schema_yaml is None:
                raise ValueError(f"Schema file not loaded or is empty: {SCHEMA_FILE_PATH}")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    #if number of columns matches schema:
    def valid_no_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = self._schema_yaml['columns']
            status = len(dataframe.columns) == len(expected_columns)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    #if all expected columns exist:
    def is_column_exists(self, dataframe: pd.DataFrame) -> bool:
        try:
            missing_num_columns = [col for col in self._schema_yaml['numeric_columns'] if col not in dataframe.columns]
            missing_cat_columns = [col for col in self._schema_yaml['categorical_columns'] if col not in dataframe.columns]

            if missing_num_columns:
                logging.info(f'Missing numeric columns: {missing_num_columns}')
            if missing_cat_columns:
                logging.info(f'Missing categorical columns: {missing_cat_columns}')

            status = not (len(missing_num_columns) > 0 or len(missing_cat_columns) > 0)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame) -> bool:
        try:
            report = Report([DataDriftPreset()],include_tests="True")
            report = report.run(reference_data=reference_df, current_data=current_df)
            report.save_html("data_drift_report.html")
            json_report = report.json()
            report_dict = json.loads(json_report)
            write_yaml_file(
                file_path=self.data_validation_config.data_validation_report,
                content=report_dict)
            
            n_features = sum(1 for m in report_dict["metrics"] if "ValueDrift" in m["metric_id"])
            drift_metric = next(m for m in report_dict["metrics"] if "DriftedColumnsCount" in m["metric_id"])
            n_drifted_features = drift_metric["value"]["count"]
            # Dataset drift status
            drift_status = n_drifted_features > 0
            print(n_features, n_drifted_features, drift_status)
            logging.info(f"{n_drifted_features}/{n_features} features show drift.")
            return drift_status    
        except Exception as e:
            logging.info(f"Error in dataset drift detection: {e}")
            raise NetworkSecurityException (e,sys)
  
    # Static method to read CSV
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)
    
    def init_data_validation(self) -> Data_validation_Artifact:
        try:
            valid_message_error = []
            # Read train and test data
            train_data = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_data = self.read_data(self.data_ingestion_artifact.test_file_path)
            # train data
            if not self.valid_no_columns(train_data):
                valid_message_error.append('Error: Column Mismatch in train data')
            if not self.is_column_exists(train_data):
                valid_message_error.append('Error: Missing columns in train data')
            #test data
            if not self.valid_no_columns(test_data):
                valid_message_error.append('Error: Column Mismatch in test data')
            if not self.is_column_exists(test_data):
                valid_message_error.append('Error: Missing columns in test data')

            # Drift detection
            validation_status = len(valid_message_error) == 0
            if validation_status:
                drift_status = self.detect_dataset_drift(train_data, test_data)
                if drift_status:
                    valid_message_error.append('Drift detected')
                else:
                    valid_message_error.append('Drift not detected')
            else:
                logging.info(f'Validation errors: {valid_message_error}')

            #Create artifact
            data_validation_artifact = Data_validation_Artifact(
                validation_status=validation_status,
                message_error=valid_message_error,
                drift_report_file_path=self.data_validation_config.data_validation_report
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

