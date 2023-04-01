from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json


def test_kafka_producer():
    try:
        KafkaProducer(
            bootstrap_servers='localhost:9093',
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii'))
    except NoBrokersAvailable:
        assert False, "Could not connect to Kafka broker"
