import json
import requests
import pandas as pd

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

def publicar_producto(access_token):
    df = pd.read_excel("productos_prueba.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    for index, row in df.iterrows():
        url = "https://api.mercadolibre.com/items"
        headers = {
        "Authorization" : f"Bearer {access_token}",
        "Content-type" : "application/json"
         }
        datos_productos = {
            "title": row["title"],
            "category_id": row["category_id"],
            "price": int(row["price"]),
            "currency_id": "ARS",
            "available_quantity": int(row["available_quantity"]),
            "buying_mode": "buy_it_now",
            "condition": "new",
            "listing_type_id": "gold_special",
            "description": {"plain_text": row["description"]},
            "attributes": [
                {"id": "BRAND", "value_name": row["marca"]},
                {"id": "MODEL", "value_name": row["modelo"]}
            ],
            "pictures": [
                {"source": row["image_url"]}
            ]
        }

        response = requests.post(url, json=datos_productos, headers=headers)
        if response.status_code == 201:
            print(f"Producto publicado correctamente: {row["title"]}")   
            print(response.json())
        else:
            print(f"Producto no publicado, error: {response.status_code}")
            print(response.json())

def obtener_categorias(access_token):
    url = "https://api.mercadolibre.com/sites/MLA/categories"

    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    res = requests.get(url, headers=headers)
    json_bonito = json.dumps(res.json(),indent=4)
    print(json_bonito)


if __name__ == '__main__':
    tokens = leer_tokens()
    access_token, refresh_token_actual = tokens["access_token"], tokens["refresh_token"]
    obtener_refresh_token(refresh_token_actual)
    #obtener_categorias(access_token)
    publicar_producto(access_token)