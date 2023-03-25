import pendulum
import os
from airflow.exceptions import AirflowConfigException
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator
)

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_ID = os.environ.get("GCP_GCS_BUCKET")


@dag(
    schedule="@once",
    start_date=pendulum.today(),
    catchup=True,
    max_active_runs=1,
    tags=["gcs", "bigquery"]
)
def create_tables_in_bigquery_from_gcs_v1():
    """
    DAG creates an empty dataset in BigQuery
    """

    @task()
    def get_prefix_from_params() -> str:
        """Gets prefix of files from DAG-run parameters
        and returns a string with prefix.
        When aren't some of parameters, then
        an AirflowConfigException will be raised.
        """
        context = get_current_context()
        params = context.get('params', {})
        prefix = params.get('prefix')
        if not prefix:
            raise AirflowConfigException(
                "There aren't required parameters in DAG-run."
                "Please check configuration of your run.")
        return prefix

    @task()
    def get_dataset_name_from_params() -> str:
        """Gets dataset_name of files from DAG-run parameters
        and returns a string with dataset_name.
        When aren't some of parameters, then
        an AirflowConfigException will be raised.
        """
        context = get_current_context()
        params = context.get('params', {})
        dataset_name = params.get('dataset_name')
        if not dataset_name:
            raise AirflowConfigException(
                "There aren't required parameters in DAG-run."
                "Please check configuration of your run.")
        return dataset_name

    prefix = get_prefix_from_params()
    dataset_name = get_dataset_name_from_params()
    path = f"data/historical_temperatures/{prefix}*"
    tablename = f"{PROJECT_ID}.{dataset_name}.{prefix}"
    create_in_bigquery = GCSToBigQueryOperator(
            task_id="create_table_in_bigquery",
            bucket=BUCKET_ID,
            source_objects=[path],
            destination_project_dataset_table=tablename,
            source_format="PARQUET",
            autodetect=True,
    )

    prefix >> dataset_name >> create_in_bigquery


create_tables_in_bigquery_from_gcs_v1()
