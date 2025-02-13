import requests
import json
 
# Parámetros para la autenticación
client_id = 'ec33621b66a14a61b82980d29cb72a4f'
client_secret = '96db5e64c8c048a6a6cd040bab0cf937'

# Obtener un token de autenticación desde spotify
auth_url = f"https://accounts.spotify.com/api/token"
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'Content-Type': 'application/x-www-form-urlencoded'
}
 
auth_response = requests.post(auth_url, data=auth_data)
access_token = auth_response.json().get("access_token")


list_id = "1hcdI2N1023RvSwLzTtdsp?si=MC2acqSwSamsMRjrUpVjwg"
# URL de la API para obtener los elementos de la lista
list_url = f"https://api.spotify.com/v1/artists/{list_id}"
 
# Realizar la petición
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(list_url, headers=headers)
 
# Mostrar los datos de la lista
list_data = response.json()
print(json.dumps(list_data, indent=2))
#rint(response.content)

'''
# Guardar los datos en un archivo JSON
with open('list_data.json', 'w') as f:
    json.dump(list_data, f)
    
    '''
