# airflow_duckdb
Sample Airflow DAG with DuckDB for data analysis


## Setup steps

#### Install Astro CLI (Airflow)

I have used astro CLI to setup Airflow server (docker) locally. It is possible to use docker directly to setup Airflow. 
However, astro CLI can help reduce the setup time drastically.

> **NOTE** Please note, docker desktop is a prerequisite to use Astro CLI for setting up local Airflow server.

Please check the documentation for installing Astro CLI - [Install the Astro CLI](https://docs.astronomer.io/astro/cli/install-cli?tab=windowswithwinget#install-the-astro-cli)


#### Get started with Airflow (using Astro CLI)

Documentation - [Get started](https://docs.astronomer.io/astro/cli/get-started-cli)

> **NOTE** You need to have Git installed on your computer to be able to clone the repository.

Setup command (windows):

```cmd


mkdir "C:\Users\<username>\Git"
cd C:\Users\<username>\Git

git clone git@github.com:basusaptarshi89/airflow_duckdb.git

cd airflow_duckdb

astro dev init

copy resources\dags\ dags\
mkdir include\sql
copy resources\include\sql\ include\sql\
copy resources\requirements.txt requirements.txt

astro dev start



```

The last command (astro dev start) should start the docker containers for Airflow server.

![astro dev start](./resources/images/astro_dev_start.png "astro dev start")


#### Generate Kaggle API key/token

The sample dataset used in this project is downloaded from Kaggle (https://www.kaggle.com/datasets/rahulvyasm/netflix-movies-and-tv-shows). The choice of dataset is completely random. However, if you decide to use a different dataset, please ensure to check the column names and adjust the SQL statements accordingly.


Create your free account on Kaggle (https://www.kaggle.com/) and create API key.

Once you are logged in to the website, on top right corner you will find your profile. Got to settings and generate the API key.

Clicking on the "Create New Token" button will download 'kaggle.json' file.

```json
{"username":"your_username","key":"yourapikey"}

```

![Kaggle API key generation](./resources/images/create_kaggle_api_key.png "Kaggle API key generation")


#### Copy the Kaggle API key file to Airflow docker container

The API key file (generated in the last step), need to be copied to the Airflow docekr container.

You will be able to view all the containers running on your machine using the following command.

```cmd

docker ps


(base) C:\Users\basus\Git\airflow_duckdb>docker ps
CONTAINER ID   IMAGE                                  COMMAND                  CREATED          STATUS                    PORTS                      NAMES
e4f0bf5ea3e5   airflow-duckdb_ff8179/airflow:latest   "tini -- /entrypoint…"   23 minutes ago   Up 23 minutes (healthy)   127.0.0.1:8080->8080/tcp   airflow-duckdb_ff8179-webserver-1
f1923f64ae38   airflow-duckdb_ff8179/airflow:latest   "tini -- /entrypoint…"   23 minutes ago   Up 23 minutes                                        airflow-duckdb_ff8179-scheduler-1
3b07dc0a685c   airflow-duckdb_ff8179/airflow:latest   "tini -- /entrypoint…"   23 minutes ago   Up 22 minutes                                        airflow-duckdb_ff8179-triggerer-1
e1fbb9684e3f   postgres:12.6                          "docker-entrypoint.s…"   23 minutes ago   Up 23 minutes             127.0.0.1:5432->5432/tcp   airflow-duckdb_ff8179-postgres-1


``` 