import productos
import json
import requests
clientId = '8118831917005061'
secretKey = 'eWOOQBL6aNCgWcSLFvFsfEkBEZOXak2h'
redirectURI = 'https://www.example.com/'

def obtener_refresh_token(refresh_token):
    url = "https://api.mercadolibre.com/oauth/token"

    payload = {
        'grant_type': 'refresh_token',
        'client_id' : clientId,
        'client_secret' : secretKey,
        'refresh_token' : refresh_token
    }
    headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        print('nuevo access token:', data.get('access_token')),
        print('nuevo refresh token:', data.get('refresh_token'))
        datos =  data.get('access_token'), data.get('refresh_token')
        with open("tokens.json", "w") as archivo:
            datos = {
                "access_token": data.get('access_token'),
                "refresh_token": data.get('refresh_token')
            }
            json.dump(datos, archivo)
        return datos

def leer_tokens():
    with open("tokens.json", "r") as archivo:
        datos_tokens = json.load(archivo)
    return datos_tokens

def publicar_producto(datos_productos, access_token):
    url = "https://api.mercadolibre.com/items"
    headers = {
        "Authorization" : f"Bearer {access_token}",
        "Content-type" : "application/json"
    }
    response = requests.post(url, json=datos_productos, headers=headers)
    if response.status_code == 201:
        print("Producto publicado correctamente")   
        print(response.json())
    else:
        print(f"Producto no publicado, error: {response.status_code}")
        print(response.json())


if __name__ == '__main__':
    tokens = leer_tokens()
    access_token, refresh_token_actual = tokens["access_token"], tokens["refresh_token"]
    datos_productos = productos.payload
    obtener_refresh_token(refresh_token_actual)
    publicar_producto(datos_productos, access_token)