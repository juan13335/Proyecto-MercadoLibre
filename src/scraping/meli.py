from bs4 import BeautifulSoup as bs
import requests

url = "https://listado.mercadolibre.com.ar/pagina/anibalengo/#global_position=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = bs(response.text, 'html.parser')
productos = soup.find_all("li", class_="ui-search-layout__item")#Tener en cuenta que esto puede dejar de funcionar ya que pueden cambiar las clases
hrefs = []

for p in productos:
    h3 = p.find("h3") #El HTML puede ir cambiando con el tiempo, por eso es mejor hacerlo de esta manera
    if h3 and h3.find("a"):
        titulo = h3.find("a").text.strip() #Permite extraer el texto sin ningun espacio
    if h3:
        a_tag = h3.find("a")
        if a_tag and a_tag.get("href"):
            hrefs.append(a_tag["href"]) #Agrega los enlaces de cada producto para luego podes extraer la descripcion detallada de cada uno


    