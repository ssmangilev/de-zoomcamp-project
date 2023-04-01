# DataTalksClub DE Zoomcamp
![Link to task](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_7_project)
## DWD-Weatherdata project

[![Link to dataset](https://www.dwd.de/EN/ourservices/cdc/cdc_ueberblick-klimadaten_en.html)](https://www.dwd.de/EN/ourservices/cdc/cdc_ueberblick-klimadaten_en.html)

A Problem, that I chose is straightforward but is also very important. It is climate change. In the example of Germany, I would like to show, that this problem is real. I used a dataset from https://www.dwd.de/EN/ourservices/cdc/cdc_ueberblick-klimadaten_en.html, thanks for this opportunity. I chose to use some pre-aggregated historical data from 1961 to nowadays.  Also as a stream part of my project, I used some real-time data about precipitation.

## Dashboard
![Dashboard_picture]((https://ibb.co/LCQfzWM))


# Technologies

  ## Infrastructure
    - Terraform - for building cloud part of the project in my case in Google Cloud Platform
    - Docker - for building "local" part of the project, where you want
  1. At first you should prove you have a terraform installed locally. You could do it with this command on linux ```terraform --version ```. On Windows/ MacOS and others OS please check ![Terraform site](https://developer.hashicorp.com/terraform/downloads).
  2. In the file ```variables.tf``` you should setup your own variables.
  3. Other steps are clearly written in the manual from DataTalksClub, you could check it here: ![Terraform Setup DataTalksClub](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp)
  4. In file ```./build/docker-compose.yaml ``` You should minimum setup your CGP-credentials and GCP-variables: ```GCP_PROJECT_ID ``` and ```GCP_GCS_BUCKET```. Without these changes you can't run all of the containers.
  5. After Setup just go to ``` ./build ``` and run a command ```docker-compose build```, after that you can run ```docker-compose up -d``` (I am waiting, that you already have ```docker``` and ```docker-compose```, and when you use Windows or MacOS, then you could use ```docker``` in this OS without external help.)
  ## Docker-compose content
File contents all airflow images, and also images to spark-cluster and kafka-cluster with kafka-ui as user interface. You could change every port, when you want to do it. Of course after changes please run again ```docker compose down``` and ```docker-compose run -d```. When you would like to change something in the ```Dockerfile``` or in the ```requirements.txt```, then please run after that ```docker-compose build``` once again.

# Batch-part of the project
  ## Workflow
  As workflow in the project is used Airflow. For the running check please the section ```Docker-compose content```. After running ```docker compose up -d``` the user interface should be on the address http://host:8080 by default. So when you're trying to run it locally, then the address would be ```http://localhost:8080```. The user and the password by default are ```airflow```.
  All dags could be runnable with parameters. All of them are in the folder ```./build/dags/``` From UI you should provide these parameters with the help of ```Trigger DAG with a config``` and there set up all parameters to ```json```. For Example for the DAG ```create_empty_dataset_in_bigquery_v1``` should be set the parameter ```dataset_name```.
  ```create_external_tables_from_gcs_files_dag_v1``` is waiting for parameters ```prefix``` and ```dataset_name``` and ```dwd_historical_data_v1``` is waiting for ```years_string``` and ``` filename```. For the last one as ```years_string``` should be one of the values: ```mean_61-90```, ```mean_71-00```, ```mean_81-10```, ```mean_91-20```. The filename should be one of ```Eistage_1961-1990.txt```, ```Frosttage_1961-1990.txt```, ```Heissetage_1961-1990.txt ```, ```Niederschlag_1961-1990.txt```, ```Sommertage_1961-1990.txt```, ``` Sonnenscheindauer_1961-1990.txt ```, ```Temperatur_1961-1990.txt ```. When ```years_string``` or ```filename``` are different from these values, it'll raise an error.
  All of DAGS are with a setting ```schedule=@once```, this means, that you should run everytime DAGS manually. ```dwd_historical_data_v1``` loads data from web to gcs. ```create_empty_dataset_in_bigquery_v1``` creates an empty dataset in bigquery DWH. ```create_external_tables_from_gcs_files_dag_v1``` uploads data from GCS-datalake to biqguery tables.

  ## Data-Transformation and Versioning
  For these purposes in the project is used DBT. You can find everywhere in the ```./dbt``` folder. The Folder contains some ```.csv``` files with a constant data and also description of the models. For checking DBT please set up your own project and just copy code from ``` ./dbt``` folder.

# Streaming-part of the project

  ## Kafka local cluster
  Kafka was used for saving a messages from producers and for allowing of reading these messages to consumers. There are two test topics, it was in ```docker-compose.yaml``` described and you could change it, if you want to do it. By default UI of kafka availible on
  ```http://localhost:8888```. Kafka-producer was described in the file ```./streaming/producer/producer.py```. Kafka-consumer was described in the file ```./streaming/consumer/consumer.py```. For the run of producer just execute ```python3 ./streaming/producer/producer.py```, for the run of consumer check please all arguments, with which this script should be run: ```python3 consumer.py --credentials_path="~/google_credentials.json" --topic="test_topic" --bootstrap_servers="localhost:5555" --bq_project="test" --bq_dataset="foo" --bq_table="bar"```
  ## Spark-cluster with pyspark
  I used spark-cluster for aggregation a real-time data. The technology names spark-streaming.
  This spark-job in file ```./streaming/spark-stream.py``` For the executing just run ```python3 ./streaming/spark-stream.py```
  ## For testing the streaming-part of the project please run producer, spark-stream and consumer together. Of course kafka should collect some data from producer at the first topic, spark-strem should write some aggregated data from the first to the second topic and consumer should write this aggregated data to BigQuery.

## CI/CD
All of python files have some basic tests, as CI/CD is used ```Github Actions```. You can find all kind of information in the ```./github/workflows/``` folder. The folder contents a couple of ```.yaml ``` files. In these files were described how airflow dags shoud be tested and how all of other python files should be tested. In the future a delpoy step would be added. All tests are run with ```pytest ```


## Python packages
You can find all of python packages in the ```requirements.txt```


## Any other questions
When you have some questions, you could ask me in telegram: ```@hh8814hh```. Thanks for your attention.
