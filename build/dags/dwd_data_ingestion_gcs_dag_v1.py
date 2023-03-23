import os
import pandas as pd
import pendulum

from airflow.exceptions import AirflowConfigException
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator
)

from pyarrow import parquet, Table

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

DATASET_URL = (
    "https://opendata.dwd.de/climate_environment/"
    "CDC/observations_germany/climate/multi_annual/"
)
PATH_TO_LOCAL_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'germany_temp_data_all')


@dag(
    schedule="@once",
    start_date=pendulum.today(),
    catchup=True,
    max_active_runs=3,
    tags=["germany_temp_historical_data"]
)
def dwd_historical_data_v1():
    """
    DAG for an upload historical data from DWD
    https://www.dwd.de/EN/ourservices/cdc/cdc_ueberblick-klimadaten_en.html
    and saving this data into GCS
    :param years_string: string with years for downloading, required
    :param filename: filename for downloading, required
    """

    @task()
    def make_download_url() -> str:
        """Builds download url from
        incoming parameters of DAG-run
        and returns a complete url string.
        When aren't some of parameters, then
        an AirflowConfigException will be raised.
        """
        context = get_current_context()
        dag_run = context.get('dag_run')
        if dag_run and hasattr(dag_run, "conf"):
            conf = dag_run.conf
            years_string = conf.get('years_string')
            filename = conf.get('filename')
            if not years_string or not filename:
                raise AirflowConfigException(
                    "There aren't required parameters in DAG-run."
                    "Please check configuration of your run.")
            return f"{DATASET_URL}{years_string}/{filename}"

    @task()
    def read_data_from_txt(src: str) -> pd.DataFrame:
        """Reads data from a txt-file
        and returns pandas.DataFrame as a result
        """
        df = pd.read_csv(src)
        return df

    @task()
    def read_filename_from_context() -> str:
        """Reads filename variable from DAG-run context"""
        context = get_current_context()
        return context.get('filename')

    @task()
    def get_parquet_filename() -> str:
        """Returns filename"""
        context = get_current_context()
        filename = context.get('filename')
        return filename.replace(".txt", ".parquet")

    @task()
    def write_data_from_dataframe_to_parquet(
            df: pd.DataFrame, filename: str) -> str:
        """
        Writes data from a pandas.DataFrame to parquet file
        , saves it local and returns a local path
        """
        save_path = f"{PATH_TO_LOCAL_HOME}{filename}.parquet"
        table = Table.from_pandas(df)
        parquet.write_table(table, save_path)
        return save_path

    download_filename = make_download_url()
    filename = read_filename_from_context()
    wget_bash = f"wget {download_filename} -O {PATH_TO_LOCAL_HOME}{filename}"
    extract = BashOperator(
        task_id="download_file_from_url",
        bash_command=wget_bash
    )
    dataframe = read_data_from_txt(
        f"{PATH_TO_LOCAL_HOME}{filename}")
    parquet_filename = get_parquet_filename()
    local_path_to_parquet = write_data_from_dataframe_to_parquet(
        dataframe, parquet_filename)
    loading = LocalFilesystemToGCSOperator(
        task_id="upload_file_to_cgs",
        src=f"{PATH_TO_LOCAL_HOME}/{parquet_filename}",
        dst=f"data/historical_temperatures/{parquet_filename}",
        bucket=BUCKET)

    download_filename >> extract >> dataframe >> parquet_filename >> local_path_to_parquet >> loading # NOQA


dwd_historical_data_v1()
