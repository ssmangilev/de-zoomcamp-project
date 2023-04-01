import json
import os
import zipfile
from io import BytesIO
from urllib.request import urlopen

import httplib2
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer

from kafka import KafkaProducer

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
                            msg_row = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}"  # NOQA: E501
                            msg = producer.send(
                                'temperature_topic',
                                key=row[0],
                                value=msg_row)
                            producer.flush()
                        os.remove(file)
