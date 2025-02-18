import pandas as pd
import pendulum
import requests
import json

from airflow.models.dag import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator

from conn_spotify import obtener_token

def extract():
   
   access_token = obtener_token()

   # ID del artista en spotify
   list_id = "1hcdI2N1023RvSwLzTtdsp?si=MC2acqSwSamsMRjrUpVjwg"
   # URL de la API para obtener los elementos de la lista
   list_url = f"https://api.spotify.com/v1/artists/{list_id}"
   
   # Realizar la petición
   headers = {"Authorization": f"Bearer {access_token}"}
   response = requests.get(list_url, headers=headers)
   list_data = response.json()
   return list_data


def transform(ti) -> list:
    artista = ti.xcom_pull(task_ids=["extract"])[0]
    
    # Mostrar los datos de la lista
    list_data = artista
   
    return list_data


def load(ti):
    list_data = ti.xcom_pull(task_ids=["transform"])[0]
    
   # Mostrar los datos de la lista
    json_data = json.dumps(list_data, indent=2)
    print(json_data)

    # Guardamos en un archivo en formato json
    archi1 = open("datos.txt", "w", encoding="utf-8")
    archi1.write(json_data)
    archi1.close()


with DAG(
   dag_id="spotify_http_op_dag",
   schedule="30 8 * * *",
   start_date=pendulum.datetime(2022, 1, 1, tz='UTC'),
   catchup=False
):

    extract = PythonOperator(
       task_id="extract",
       python_callable=extract,       
    )

    transform = PythonOperator(
       task_id='transform',
       python_callable=transform,
    )

    load = PythonOperator(
       task_id='load',
       python_callable=load,
    )

    extract >> transform >> load
