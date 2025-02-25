import requests
import json
import pandas as pd

# Parámetros para la autenticación
client_id = 'ec33621b66a14a61b82980d29cb72a4f'
client_secret = '60d805e032644956920b52182685deb0'
scope = 'playlist-read-private'
redirect_uri = 'https://localhost-api/'

def obtener_code(c):
    # Parámetros para la autenticación
    client_id = 'ec33621b66a14a61b82980d29cb72a4f'
    client_secret = '60d805e032644956920b52182685deb0'
    scope = 'playlist-read-private'
    redirect_uri = 'https://localhost-api/'


    auth_data = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }

def obtener_token():

    # Parámetros para la autenticación
    client_id = 'ec33621b66a14a61b82980d29cb72a4f'
    client_secret = '60d805e032644956920b52182685deb0'

    # Obtener un token de autenticación desde spotify
    auth_url = f"https://accounts.spotify.com/api/token"
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'Content-Type': 'application/x-www-form-urlencoded',
        'scope': 'playlist-read-private'
    }
    
    auth_response = requests.post(auth_url, data=auth_data)
    access_token = auth_response.json().get("access_token")
    #print(auth_response.json())
    return access_token

def descargar_artista(access_token):

    list_id = "1hcdI2N1023RvSwLzTtdsp?si=MC2acqSwSamsMRjrUpVjwg"
    # URL de la API para obtener los elementos de la lista
    list_url = f"https://api.spotify.com/v1/artists/{list_id}"
    
    # Realizar la petición
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(list_url, headers=headers)
    
    # Mostrar los datos de la lista
    list_data = response.json()
    print(json.dumps(list_data, indent=2))
    json_data = json.dumps(list_data, indent=2)
    
    # Guardamos en un archivo en formato json
    archi1 = open("datos.txt", "w", encoding="utf-8")
    archi1.write(json_data)
    archi1.close()

def descargar_playlist(access_token):

    # URL de la API para obtener la playlist del usuario
    url = "https://api.spotify.com/v1/me/tracks"

    # Realizar la petición
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    # Mostrar código de respuesta
    #print(response)
    
    # Mostrar los datos de la lista
    list_data = response.json()
    print(json.dumps(list_data, indent=2))
    #json_data = json.dumps(list_data, indent=2)

if __name__ == '__main__':    
    token = obtener_token()
    descargar_playlist(token)
    #descargar_artista(token)
