import pendulum
import os
from airflow.exceptions import AirflowConfigException
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator
)

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")


@dag(
    schedule="@once",
    start_date=pendulum.today(),
    catchup=True,
    max_active_runs=1,
    tags=["create_empty_dataset_in_bigquery"]
)
def create_empty_dataset_in_bigquery_v1():
    """
    DAG creates an empty dataset in BigQuery
    """

    @task()
    def get_dataset_name_from_params() -> str:
        """Gets dataset name from DAG-run parameters
        and returns a string with dataset name.
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

    @task()
    def create_empty_dataset(dataset_name: str):
        """Creates an empty dataset in BigQuery"""
        BigQueryCreateEmptyDatasetOperator(
            project_id=PROJECT_ID,
            task_id=f"create_empty_dataset_{dataset_name}",
            dataset_id=dataset_name,
            location="europe-west6"
        ).execute(context=None)

    name = get_dataset_name_from_params()
    created_dataset = create_empty_dataset(name)

    name >> created_dataset


create_empty_dataset_in_bigquery_v1()
