
import argparse
from decimal import Decimal
from pathlib import Path

from google.cloud import bigquery, exceptions
from google.oauth2 import service_account
from kafka import KafkaConsumer
from kafka import errors as kafka_errors


def main(params):
    credentials = params.credentials_path
    topic = params.topic
    bootstrap_servers = params.bootstrap_servers
    bq_project = params.bq_project
    bq_dataset = params.bq_dataset
    bq_table = params.bq_table
    if not credentials or not topic \
            or not bootstrap_servers or not bq_table \
            or not bq_dataset or not bq_project:
        raise ValueError('Missing required parameters')
    credentials = credentials.replace("~", str(Path.home()))
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset='earliest',
        enable_auto_commit=True)
    creds = service_account.Credentials.from_service_account_file(credentials)
    bq_client = bigquery.Client(credentials=creds)
    table_ref = bq_client.dataset(
        project=bq_project, dataset_id=bq_dataset).table(bq_table)
    try:
        table = bq_client.get_table(table_ref)
        print("Table found")
    except exceptions.NotFound:
        print("Table not found, creating table...")
        schema = [
            bigquery.SchemaField("stations_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("rs_01", "FLOAT64", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp",  # name of column to use for partitioning
            expiration_ms=7776000000,
        )  # 90 days
        table = bq_client.create_table(table)
        print("Table created")
    schema = table.schema
    batch_to_bq = []
    try:
        for message in consumer:
            batch_to_bq.append({
                'stations_id': message.key.decode('utf-8'),
                'rs_01': Decimal(message.value.decode('utf-8')),
                'timestamp': message.timestamp / 1000})
            if len(batch_to_bq) >= 50:
                errors = bq_client.insert_rows(
                    table, batch_to_bq, selected_fields=schema)
                if errors:
                    raise ValueError(errors)
                print("Inserted 50 rows")
                batch_to_bq.clear()
    except kafka_errors.NoBrokersAvailable:
        print('No brokers available.')
    except kafka_errors.KafkaTimeoutError:
        print("Timeout error.")
    except kafka_errors.OffsetOutOfRangeError:
        print("Offset out of range error.")
    except kafka_errors.CommitFailedError:
        print("Commit failed error.")
    except kafka_errors.IllegalStateError:
        print("Illegal state error.")
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Consumer to kafka topic")
    # credentials_path
    # topic
    # bootstrap_servers
    # bq_table
    parser.add_argument('--credentials_path', type=str)
    parser.add_argument('--topic', type=str)
    parser.add_argument('--bootstrap_servers',
                        type=str, default='localhost:9093')
    parser.add_argument('--bq_project', type=str)
    parser.add_argument('--bq_dataset', type=str)
    parser.add_argument('--bq_table', type=str)
    args = parser.parse_args()
    main(args)
