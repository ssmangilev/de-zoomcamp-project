import pyspark.sql.types as T

BOOTSTRAP_SERVERS = 'localhost:9092'

SPARK_TOPIC = 'pyspark_agregated_topic'

PRODUCE_TOPIC = CONSUME_TOPIC = 'temperature_topic'

MESSAGES_SCHEMA = T.StructType(
    [T.StructField("STATIONS_ID", T.IntegerType()),
     T.StructField('MESS_DATUM', T.TimestampType()),
     T.StructField('QN', T.IntegerType()),
     T.StructField("RS_01", T.FloatType()),
     T.StructField("RS_IND_01", T.FloatType()),
     T.StructField("eor", T.StringType()),
     ])
