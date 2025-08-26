import requests
from bs4 import BeautifulSoup as bs

url = "https://listado.mercadolibre.com.ar/pagina/anibalengo/#global_position=1"

headers = {
    "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

response = requests.get(url, headers)
soup = bs(response.text, "html.parser")
productos = soup.find_all("li", class_="ui-search-layout__item")

def obtener_titulo(productos):
    hrefs = []
    titulo = []
    for p in productos:
        try:
            h3 = p.find("h3") #El HTML puede ir cambiando con el tiempo, por eso es mejor hacerlo de esta manera
            if h3 and h3.find("a"):
                titulo_text = h3.find("a").text.strip()
                titulo.append(titulo_text) #Permite extraer el texto sin ningun espacio
            if h3:
                a_tag = h3.find("a")
                if a_tag and a_tag.get("href"):
                    hrefs.append(a_tag["href"]) #Agrega los enlaces de cada producto para luego podes extraer la descripcion detallada de cada uno
        except Exception as e:
            print(f"Error: {e}")
            continue
    print(titulo) 

def obtener_descripcion(hrefs, headers):
    descripciones = []
    
    for link_producto in hrefs:
        try:
            response = requests.get(link_producto, headers=headers)
            soup = bs(response.text, 'html.parser')
            seccion = soup.find(id="description")
            if seccion:
                p_tag = seccion.find("p")
                if p_tag:
                    descripciones.append(p_tag.text.strip())
                else:
                    descripciones.append("No disponible")  
            else:
                descripciones.append("No disponible")  
        except Exception as e:
            print(f'Error en {link_producto}: {e}')
            descripciones.append("Error")
    
    return descripciones
