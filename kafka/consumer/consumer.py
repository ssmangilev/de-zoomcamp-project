from pyspark.sql import SparkSession

from pyspark.sql.functions import *
from pyspark.sql.types import *

import os

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 pyspark-shell'

spark = SparkSession \
    .builder \
    .appName("Kafka-Spark-Stream") \
    .config("spark.sql.debug.maxToStringFields", 100) \
    .getOrCreate()

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9093") \
    .option("subscribe", "temperature_topic") \
    .option("includeHeaders", "true") \
    .option("startingOffsets", "earliest") \
    .option("spark.streaming.kafka.maxRatePerPartition", 100) \
    .load()

import pdb;pdb.set_trace()