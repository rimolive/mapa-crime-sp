import pandas
import requests
import json
import googlemaps

GMAPS_API_KEY = '' # Preencha aqui a API Key do Google Maps.

gmaps = googlemaps.Client(key=GMAPS_API_KEY)
# GMaps API Docs:
# https://developers.google.com/maps/documentation/javascript/marker-clustering

YEAR = "2017"
MONTH = "07"
CRIME = ""
BASE_PATH = "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/database"
SPATIAL_PATH = "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/spatial"
FILE = "{}_{}_{}.csv"
LOCATION = ""

def filtra_dados_anos(crime):
    for year in range(2003,2017):
        YEAR = str(year)
        raw_path = "{}/{}/".format(BASE_PATH, YEAR)
        filtra_dados_cidade(raw_path, crime, YEAR)

def filtra_dados_cidade(raw_path, crime, year=0):
    if len(MONTH) > 0:
        dados = pandas.read_csv(raw_path + FILE.format(crime, YEAR, MONTH), na_values='', delimiter=',', header=0)
        gera_arquivo_coordenadas(dados, raw_path, crime, YEAR, MONTH)
    else:
        for month in range(1,12):
            smonth = format(month, '02d')
            dados = pandas.read_csv(raw_path + FILE.format(crime, YEAR, smonth), na_values='', delimiter=',', header=0)
            gera_arquivo_coordenadas(dados, raw_path, crime, YEAR, smonth)

def gera_arquivo_coordenadas(dados, path, crime, year, month):
    if len(LOCATION) > 0:
        dados = dados[dados['CIDADE'] == LOCATION]
    dados['ENDERECOCOMPLETO'] = dados['LOGRADOURO'] + ', ' + dados['NUMERO'].apply(str) + ' ' + dados['BAIRRO'] + ' - ' + dados['CEP'] + ' ' + dados['CIDADE'] + ' ' + dados['UF']
    dados['COORDENADAS'] = dados['ENDERECOCOMPLETO'].apply(recupera_coordenadas_mapa)

    dados.to_csv(SPATIAL_PATH + FILE.format(crime, year, month))

def recupera_coordenadas_mapa(address):
    # print address
    return gmaps.geocode(address)

if __name__ == '__main__':
    if len(CRIME) > 0:
        if len(YEAR) > 0:
            raw_path = "{}/{}/".format(BASE_PATH, YEAR)
            filtra_dados_cidade(raw_path, CRIME)
        else:
            filtra_dados_anos(CRIME)
    else:
        for crime in ['furtocelular', 'furtoveiculo', 'homicicio', 
                      'latrocinio', 'lesaomorte', 'mortepolicial', 
                      'mortesuspeita', 'roubocelular', 'rouboveiculo']:
            filtra_dados_anos(crime)