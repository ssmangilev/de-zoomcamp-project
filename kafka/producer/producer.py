from io import BytesIO
import pandas as pd
import zipfile
import csv
import requests
import os
import json
from kafka import KafkaProducer

import ftplib
import httplib2
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer

URL_TO_DOWNLOAD = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/1_minute/precipitation/now/" # NOQA

http = httplib2.Http()
status, response = http.request(URL_TO_DOWNLOAD)

producer = KafkaProducer(
    bootstrap_servers='localhost:9093',
    value_serializer=lambda v: json.dumps(v).encode('ascii'),
    key_serializer=lambda v: json.dumps(v).encode('ascii'))

for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
    if link.has_attr('href') and link['href'].endswith('.zip'):
        file_url = f"{URL_TO_DOWNLOAD}/{link['href']}"
        with urlopen(file_url) as zipresp:
            with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
                files = zfile.extractall()
                for file in os.listdir():
                    if 'txt' in file:
                        df = pd.read_csv(file, sep=';')
                        # for index, row in df.T.items():
                        # send message to kafka
                        for index, row in df.T.items():
                            msg = producer.send(
                                'temperature_topic', row.to_json())
                            producer.flush()
                        os.remove(file)
