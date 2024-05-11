"""
Analysis of Netflix movies/shows using Airflow and DuckDB.

The first task (download_dataset) downloads the netflix shows dataset from Kaggle using the kaggle API.
In order to use the kaggle python sdk, install the python package 'kaggle'. This is done by updating the 
requirements.txt file for this Airflow instance.

Document: https://github.com/Kaggle/kaggle-api/blob/main/docs/KaggleApi.md#datasets_download

The Kaggle API key need to be saved as a JSON file -

```bash
# list the docker containers
docker ps

# login to the docker container (scheduler)
docker exec -it <container-name> bash

var_kaggle_dir="/home/astro/.kaggle"
var_kaggle_file="${var_kaggle_dir}/kaggle.json"
mkdir -p ${var_kaggle_dir} & echo '{"username":"username","key":"apikeyblabla"}' >${var_kaggle_file} & chmod 775 ${var_kaggle_file}

```
"""

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.models.param import Param
from pprint import pprint
import zipfile
from jinja2 import Template
import kaggle 
import duckdb
import os


# #################### #
#   Utility functions
# #################### #
def get_airflow_connection(connection_name):
    conn = BaseHook.get_connection(connection_name)
    return conn


# #################################### #
#  DAG: netflix_data_analysis_duckdb
# #################################### #
@dag(
        dag_id="netflix_data_analysis_duckdb",
        start_date=None,
        schedule=None,
        catchup=False,
        doc_md=__doc__,
        params={
            "kaggle_dataset_owner": "rahulvyasm",
            "kaggle_dataset_name": "netflix-movies-and-tv-shows",
            "airflow_folder": "/usr/local/airflow/include"            
        }
)
def netflix_data_analysis_duckdb():

    @task()
    def set_folder_paths(**context):
        airflow_folder = context["params"]["airflow_folder"]
        data_folder = f"{airflow_folder}/data"
        raw_data_folder = f"{data_folder}/raw"
        database_folder = f"{data_folder}/database"
        sql_folder = f"{airflow_folder}/sql"

        os.makedirs(raw_data_folder, exist_ok=True)
        os.makedirs(database_folder, exist_ok=True)

        return {
            "data_folder": data_folder,
            "raw_data_folder": raw_data_folder,
            "database_folder": database_folder,
            "sql_folder": sql_folder
        }

    @task()
    def download_dataset(folder_paths, **context):
        """
        This task downloads the netflix dataset using kaggle api
        and save it as '/usr/local/airflow/include/data/raw/netflix.zip'

        Returns the path of the zip file.
        """
        kaggle_dataset_owner = context["params"]["kaggle_dataset_owner"]
        kaggle_dataset_name = context["params"]["kaggle_dataset_name"]

        # list the dataset (optional)
        r = kaggle.api.datasets_list_files(
            owner_slug=kaggle_dataset_owner, 
            dataset_slug=kaggle_dataset_name
        )
        pprint(r)

        # download the dataset and save as zip file
        raw_data_folder = folder_paths["raw_data_folder"]
        zip_file = f"{raw_data_folder}/netflix.zip"
        try:
            # hack: _preload_content=False
            # hack to avoid execution of "r.data = r.data.decode('utf8')" in https://github.com/Kaggle/kaggle-api/blob/main/kaggle/rest.py#L235
            # It is possible to override the default value (True) of the parameter "_preload_content"
            # This will return the raw response, instead of trying to decode the data in utf-8 format
            # https://github.com/Kaggle/kaggle-api/blob/main/kaggle/api/kaggle_api.py#L1696

            
            r = kaggle.api.datasets_download(
                owner_slug=kaggle_dataset_owner, 
                dataset_slug=kaggle_dataset_name,
                _preload_content=False 
                
            )
            with open(zip_file, "wb") as f:
                f.write(r.data)
        except Exception as e:
            print(f"Error: {e}")  
            raise e      
        return zip_file

    @task()
    def unzip_netflix_data(folder_paths, zip_file, **context):
        raw_data_folder = folder_paths["raw_data_folder"]
        csv_file_path = f"{raw_data_folder}/netflix"
        with zipfile.ZipFile(zip_file, "r") as f:
            f.extractall(csv_file_path)
        return csv_file_path
    
    @task()
    def create_duckdb_table(folder_paths, csv_file_path, **context):
        database_folder = folder_paths["database_folder"]
        sql_folder = folder_paths["sql_folder"]
        database = f"{database_folder}/netflix.db"

        # connect to database and create table
        conn = duckdb.connect(database=database)
        with open(f"{sql_folder}/create_netflix_table.sql", "r") as f:
            sql_statement = f.read()
            sql_statement = Template(sql_statement).render(csv_file_path=f"{csv_file_path}/*.csv")
        print(sql_statement)
        conn.execute(sql_statement)

    folder_paths = set_folder_paths()
    zip_file = download_dataset(folder_paths)
    csv_file_path = unzip_netflix_data(folder_paths, zip_file)
    create_duckdb_table(folder_paths, csv_file_path)


netflix_data_analysis_duckdb()
