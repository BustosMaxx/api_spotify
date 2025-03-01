import pandas as pd
import pendulum
import requests
import json
import base64

from airflow.models.dag import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator

from conn_spotify import obtener_token
# Información de tu aplicación (client_id y client_secret)
# CLIENT_ID = 'ec33621b66a14a61b82980d29cb72a4f'
# CLIENT_SECRET = '60d805e032644956920b52182685deb0'
# global refresh_token
# refresh_token = 'AQAn6pznVOcY2n97J-XxD6olKoMnd1EDbgLgFrudwu-GNxoqBeBnDonVSqrZhVaFIDvMuJDhrCQ4fT2X6-PbsiSpawVK58hc-rqpLUcsDauHfqVnPvXPe_OxdB7On71LWQ4'
authorization_base_url = 'https://accounts.spotify.com/authorize?'
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'https://localhost-api/'
scope = ['playlist-read-private', 'playlist-read-collaborative', 'user-library-read']

def refresh_access_token():
    
    """Refresca el token de acceso utilizando el refresh token."""

    CLIENT_ID = 'ec33621b66a14a61b82980d29cb72a4f'
    CLIENT_SECRET = '60d805e032644956920b52182685deb0'
    global refresh_token
    refresh_token = 'AQAn6pznVOcY2n97J-XxD6olKoMnd1EDbgLgFrudwu-GNxoqBeBnDonVSqrZhVaFIDvMuJDhrCQ4fT2X6-PbsiSpawVK58hc-rqpLUcsDauHfqVnPvXPe_OxdB7On71LWQ4'

    #global ACCESS_TOKEN, REFRESH_TOKEN

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
      #   print(ACCESS_TOKEN)
        REFRESH_TOKEN = token_info.get('refresh_token', refresh_token)  # Actualiza el refresh token si se proporciona
      #   print(REFRESH_TOKEN)
    else:
        raise Exception(f'Error refreshing token: {response.status_code}, {response.text}')
    
    return access_token

def extract():
   
   access_token = refresh_access_token()

   # URL de la API para obtener la playlist del usuario
   url = "https://api.spotify.com/v1/me/playlists"

   # Realizar la petición
   headers = {"Authorization": f"Bearer {access_token}"}
   response = requests.get(url, headers=headers)
   #response = oauth.get(url)
    
   # Mostrar código de respuesta
   #print(response)
    
   # Mostrar los datos de la lista
   list_data = response.json()
   #print(json.dumps(list_data, indent=2))
   #json_data = json.dumps(list_data, indent=2)
   
   return list_data


def transform(ti) -> list:
    artista = ti.xcom_pull(task_ids=["extract"])[0]
    
    # Mostrar los datos de la lista

    playlist = artista
    playlist_list = []
    for i in playlist['items']:
        playlist_list.append(i)
    
    columnas = list(playlist['items'][0].keys())
    playlist_df = pd.DataFrame(data = playlist_list, columns = columnas)
    playlist_df.drop([ 'external_urls', 'href', 'images', 'primary_color',
                       'snapshot_id', 'tracks', 'uri', 'owner'], axis=1, inplace = True)
   
    return playlist_df


def load(ti):
    df_data = ti.xcom_pull(task_ids=["transform"])[0]
    
   # Guardamos en un archivo en formato csv
    df_data.to_csv('tabla_playlist.csv', index=False)
    


with DAG(
   dag_id="spotify_dag",
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
