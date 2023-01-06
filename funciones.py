import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.mediotiempo.com/futbol/liga-mx/tabla-general"


def leer_url(url):
    """
    Manda request a la página de MedioTiempo y con bs4 transforma la respuesta
    a un html

    Argumentos:
        url: Url de la página web
    
    Retorna:
        Un html response en la variable soup
    """
    response = requests.get(url)

    response.encoding = 'utf-8'

    html = response.text

    soup = BeautifulSoup(html,'html.parser')

    return soup

def crear_tabla(soup):
    """
    Crea la tabla con las estadísticas de la liga MX del torneo actual y calcula
    los valores para su racha de victorias y el número de goles.

    Argumentos:
        soup: La respuesta html de bs4.

    Retorna:
        df3: Un dataframe con las estadisticas de los equipos
    """    
    all_data = soup.find_all('tr', {'class': 'ctr-stadistics-header__tr'})
    list = []
    for i in range(1,len(all_data)):
        list.append(all_data[i].text)

    lista_nueva = [ x.split('\n') for x in list]
    df2 = pd.DataFrame(lista_nueva)
    df3 = df2.drop([0,2,3,5,6,15],axis=1)
    df3 = df3.rename(columns={1:"Posición",4:"Equipo",7:"Juegos jugados",8:"Juegos ganados",
                9:"Juegos empatados",10:"Juegos perdidos",
                11:"Goles a favor",12:"Juegos en contra", 13:"Diferencia de goles", 
                14:"Puntos"})

    df3["Juegos jugados"] = pd.to_numeric(df3["Juegos jugados"])
    df3["Juegos ganados"] = pd.to_numeric(df3["Juegos ganados"])
    df3["Goles a favor"] = pd.to_numeric(df3["Goles a favor"])

    df3["Racha"] = df3["Juegos ganados"] / df3["Juegos jugados"]
    df3["Over goles"] = df3["Goles a favor"] / df3["Juegos jugados"]

    return df3