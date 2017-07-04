import pandas
import requests
import json
import googlemaps

GMAPS_API_KEY = '' # Preencha com a API Key gerada no Google.

gmaps = googlemaps.Client(key=GMAPS_API_KEY)

BASE_PATH = "" # Preencha esse valor com um caminho para gravar os arquivos xls.

YEAR = "2017"
MONTH = "05"
PATH = "{}/data/{}/".format(YEAR)
FILE = "homicidio_{}_{}.csv".format(YEAR, MONTH)
GEO_FILE = "homicidio_{}_{}_geo.csv".format(YEAR, MONTH)

def filtra_dados_cidade():
    dados = pandas.read_csv(PATH + FILE, na_values='', delimiter=',', header=0)
    dados = dados[dados['CIDADE'] == 'S.PAULO']
    dados['end_completo'] = dados['LOGRADOURO'] + ', ' + dados['NUMERO'].apply(str) + ' ' + dados['CIDADE'] + ' ' + dados['UF']
    dados['coord'] = dados['end_completo'].apply(recupera_coordenadas_mapa)

    dados.to_csv(PATH + GEO_FILE)


def recupera_coordenadas_mapa(address):
    return gmaps.geocode(address)

# def

if __name__ == '__main__':
    filtra_dados_cidade()
