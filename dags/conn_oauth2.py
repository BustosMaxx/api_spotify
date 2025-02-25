#from requests_oauthlib import OAuth2Session
from authlib.integrations.requests_client import OAuth2Session
import requests
import json
#import pandas as pd

# Información de tu aplicación (client_id y client_secret)
client_id = 'ec33621b66a14a61b82980d29cb72a4f'
client_secret = '60d805e032644956920b52182685deb0'
authorization_base_url = 'https://accounts.spotify.com/authorize?'
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'https://localhost-api/'
scope = ['playlist-read-private', 'playlist-read-collaborative', 'user-library-read']

# Crear una sesión OAuth2
oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri,scope=scope)
''''''
# Redirigir al usuario al proveedor de OAuth2 para autorizar la aplicación
authorization_url, state = oauth.create_authorization_url(authorization_base_url)
print('Por favor, abre este enlace en tu navegador: {}'.format(authorization_url))

# El usuario autoriza la aplicación e ingresa el código de autorización que obtiene
redirect_response = input('Pega la URL completa de redirección aquí: ')

#redirect_response = 'https://localhost-api/?code=AQD6cGgc6-pOfpFgUsFZOvLJq5mVcC6ukMlrczCak45gAKnKuhZVrx_XzSJpDK-kfT7LdkIxMwkdRNG803UtPPb321nSwfkrvECdYnA8gJ5PhujFmMBz8UilgO7ermOntVAqK7IEumgFXJJ4rVaI-5PaB18_2_MBSMo&state=m8kMMSY8HWunSEND2h3tC2VMdkefdt'

# Obtener el token de acceso
token = oauth.fetch_token(token_url, client_secret=client_secret,
                          authorization_response=redirect_response)

list_id = "1hcdI2N1023RvSwLzTtdsp?si=MC2acqSwSamsMRjrUpVjwg"
# URL de la API para obtener los elementos de la lista
protected_url = f"https://api.spotify.com/v1/artists/{list_id}"
# Hacer una solicitud autenticada
response = oauth.get(protected_url)
print(response.content)



def descargar_playlist(access_token):

    # URL de la API para obtener la playlist del usuario
    url = "https://api.spotify.com/v1/me/tracks"

    # Realizar la petición
    #headers = {"Authorization": f"Bearer {access_token}"}
    #response = requests.get(url, headers=headers)
    response = oauth.get(url)

    
    # Mostrar código de respuesta
    #print(response)
    
    # Mostrar los datos de la lista
    list_data = response.json()
    print(json.dumps(list_data, indent=2))
    #json_data = json.dumps(list_data, indent=2)

if __name__ == '__main__':
    print(token)
    descargar_playlist(token)