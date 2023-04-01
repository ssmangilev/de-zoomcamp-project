import os

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame, SparkSession
from settings import MESSAGES_SCHEMA
from settings import PRODUCE_TOPIC as topic
from settings import SPARK_TOPIC

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 pyspark-shell' # NOQA


def read_data_from_kafka(
        session: SparkSession, topic: str) -> DataFrame:
    return session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9093") \
        .option("subscribe", topic) \
        .option("includeHeaders", "true") \
        .option("startingOffsets", "earliest") \
        .option("spark.streaming.kafka.maxRatePerPartition", 100) \
        .load()


def parse_data_from_kafka_messages(
        df: DataFrame, schema: T.StructType) -> DataFrame:
    col = F.split(df['value'], ', ')
    for idx, field in enumerate(schema):
        df = df.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return df.select(['RS_01', 'key'])


def groupby_data(
        df: DataFrame) -> DataFrame:
    return df.groupBy("key").avg("RS_01")


def prepare_df_to_kafka_sink(df: DataFrame, value_columns):
    df = df.withColumn("value", F.concat_ws(', ', *value_columns))
    return df.select(['key', 'value'])


def sink_kafka(df, topic):
    return df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9093") \
        .outputMode('complete') \
        .option("topic", topic) \
        .option("checkpointLocation", "checkpoint") \
        .start() \
        .awaitTermination()


if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Kafka-Spark-Stream") \
        .config("spark.sql.debug.maxToStringFields", 100) \
        .getOrCreate()
    df = read_data_from_kafka(spark, topic)
    data = parse_data_from_kafka_messages(df, MESSAGES_SCHEMA)
    grouped_data = groupby_data(data)
    df_to_kafka = prepare_df_to_kafka_sink(
        df=grouped_data,
        value_columns=['avg(RS_01)'])
    result_to_kafka = sink_kafka(df_to_kafka, SPARK_TOPIC)
