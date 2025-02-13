#!/bin/bash

# Reemplazar {tenant_id}, {client_id} y {client_secret} por los valores correctos de tu aplicación registrada.

client_id=ec33621b66a14a61b82980d29cb72a4f
client_secret=96db5e64c8c048a6a6cd040bab0cf937

token=$(curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=$client_id&client_secret=$client_secret")

access_token=${token:(17)}
access_token=${access_token%%,*}
access_token=${access_token:(0):(-1)}

curl "https://api.spotify.com/v1/artists/1hcdI2N1023RvSwLzTtdsp?si=MC2acqSwSamsMRjrUpVjwg" \
     -H "Authorization: Bearer  $access_token"

echo $token
