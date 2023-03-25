from airflow.exceptions import AirflowConfigException
from airflow.models import DagBag, TaskInstance
from unittest.mock import patch
import dwd_data_ingestion_gcs_dag_v1
import pandas as pd
from pyarrow import parquet
import os


def test_dag_loaded_with_no_errors():
    dagbag = DagBag(dag_folder="../")
    assert dagbag.dags is not None
    assert dagbag.import_errors == {}


def test_dag_contains_all_tasks():
    dagbag = DagBag(dag_folder="../")
    dag_id = "dwd_historical_data_v1"
    dag = dagbag.get_dag(dag_id)
    assert dag_id == dag.dag_id
    task_ids = {"make_download_url", "read_filename_from_context",
                "get_parquet_filename", "write_data_from_dataframe_to_parquet",
                "download_file_from_url", "upload_file_to_cgs"}
    for task_id in task_ids:
        assert task_id in dag.task_ids


def test_dag_dependencies():
    dagbag = DagBag(dag_folder="../")
    dag_id = "dwd_historical_data_v1"
    dag = dagbag.get_dag(dag_id)
    download_task = dag.get_task("download_file_from_url")
    parquet_task = dag.get_task("write_data_from_dataframe_to_parquet")
    upload_task = dag.get_task("upload_file_to_cgs")
    assert parquet_task in download_task.downstream_tasks
    assert upload_task in parquet_task.downstream_tasks


def test_make_download_url():
    # There are all parameters
    with patch.object(
            TaskInstance, "xcom_pull",
            return_value={"params": {
                "years_string": "2020",
                "filename": "file.txt"}}):
        assert dwd_data_ingestion_gcs_dag_v1.make_download_url() == (
            "https://opendata.dwd.de/climate_environment/CDC/"
            "observations_germany/climate/multi_annual/2020/file.txt")

    #  There isn't years_string
    with patch.object(
            TaskInstance, "xcom_pull",
            return_value={"params": {"filename": "file.txt"}}):
        try:
            dwd_data_ingestion_gcs_dag_v1.make_download_url()
        except Exception as e:
            assert isinstance(e, AirflowConfigException)
            assert str(e) == ("There aren't required parameters in DAG-run."
                              " Please check configuration of your run.")

    # There isn't filename
    with patch.object(
            TaskInstance, "xcom_pull",
            return_value={"params": {"years_string": "2020"}}):
        try:
            dwd_data_ingestion_gcs_dag_v1.make_download_url()
        except Exception as e:
            assert isinstance(e, AirflowConfigException)
            assert str(e) == ("There aren't required parameters"
                              " in DAG-run. Please check "
                              " configuration of your run.")


def test_read_filename_from_context():
    context = {"params": {"filename": "test.txt"}}
    filename = dwd_data_ingestion_gcs_dag_v1.read_filename_from_context(
        context)
    assert filename == "test.txt"


def test_get_parquet_filename():
    context = {"params": {"filename": "test.txt"}}
    parquet_filename = dwd_data_ingestion_gcs_dag_v1.get_parquet_filename(
        context)
    assert parquet_filename == "test.parquet"


def test_write_data_from_dataframe_to_parquet(tmpdir):
    data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    df = pd.DataFrame(data)
    csv_file = tmpdir.join("test.csv")
    df.to_csv(csv_file, index=False)

    # Call the function with the test data
    filename = "test.parquet"
    path_to_parquet =\
        dwd_data_ingestion_gcs_dag_v1.write_data_from_dataframe_to_parquet(
            str(csv_file), filename)
    assert os.path.exists(path_to_parquet)
    table = parquet.read_table(path_to_parquet)
    df_from_parquet = table.to_pandas()
    pd.testing.assert_frame_equal(df, df_from_parquet)
