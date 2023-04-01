from airflow.models import DagBag


def test_dag_loaded_with_no_errors():
    dagbag = DagBag(dag_folder="./", include_examples=False)
    assert dagbag.dags is not None
    assert dagbag.import_errors == {}


def test_dwd_historical_data_v1_contains_all_tasks():
    dagbag = DagBag(dag_folder="./", include_examples=False)
    dag_id = "dwd_historical_data_v1"
    dag = dagbag.get_dag(dag_id)
    assert dag_id == dag.dag_id
    task_ids = {"make_download_url", "read_filename_from_context",
                "get_parquet_filename", "write_data_from_dataframe_to_parquet",
                "download_file_from_url", "upload_file_to_cgs"}
    for task_id in task_ids:
        assert task_id in dag.task_ids


def test_create_empty_dataset_in_bigquery_contains_all_tasks():
    dagbag = DagBag(dag_folder="./", include_examples=False)
    dag_id = "create_empty_dataset_in_bigquery_v1"
    dag = dagbag.get_dag(dag_id)
    assert dag_id == dag.dag_id
    task_ids = {"get_dataset_name_from_params", "create_empty_dataset"}
    for task_id in task_ids:
        assert task_id in dag.task_ids


def test_create_external_tables_from_gcs_files_dag_v1_contains_all_tasks():
    dagbag = DagBag(dag_folder="./", include_examples=False)
    dag_id = "create_tables_in_bigquery_from_gcs_v1"
    dag = dagbag.get_dag(dag_id)
    assert dag_id == dag.dag_id
    task_ids = {"get_prefix_from_params", "get_dataset_name_from_params",
                "create_table_in_bigquery"}
    for task_id in task_ids:
        assert task_id in dag.task_ids
