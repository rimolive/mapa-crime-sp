import pandas as pd
import math
from json import JSONDecoder

YEAR = "2003"
MONTH = ""
CRIME = "latrocinio"
GEO_PATH = "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/spatial/{}/".format(YEAR)
SITE_PATH = "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/site/"
FILE = "{}_{}_{}.csv"

def gera_massa():
	if len(MONTH) > 0:
		dados = pd.read_csv(GEO_PATH + FILE.format(CRIME, YEAR, MONTH), na_values='', delimiter=',', header=0)
		print "Generating site data for " + GEO_PATH + FILE.format(CRIME, YEAR, MONTH) + "..."
		dados['tipo'] = "Latrocinio"
		dados['data-ocorrencia'] = dados['DATAOCORRENCIA']
		dados['endereco'] = dados['LOGRADOURO'] + ', ' + dados['NUMERO'].apply(str) + ' ' + dados['BAIRRO'] + ' - ' + dados['CEP'].apply(str) + ' ' + dados['CIDADE'] + ' ' + dados['UF']
		dados['latitude'] = dados['COORDENADAS'].apply(retorna_latitude)
		dados['longitude'] = dados['COORDENADAS'].apply(retorna_longitude)

		massa = dados[['tipo','data-ocorrencia','endereco','latitude','longitude']]
		massa.to_csv(SITE_PATH + FILE.format(CRIME, YEAR, MONTH))
	else:
		for month in range(1,13):
			smonth = format(month, '02d')
			print "Generating site data for " + GEO_PATH + FILE.format(CRIME, YEAR, smonth) + "..."
			dados = pd.read_csv(GEO_PATH + FILE.format(CRIME, YEAR, smonth), na_values='', delimiter=',', header=0)
			dados['tipo'] = "Latrocinio"
			dados['data-ocorrencia'] = dados['DATAOCORRENCIA']
			dados['endereco'] = dados['LOGRADOURO'] + ', ' + dados['NUMERO'].apply(str) + ' ' + dados['BAIRRO'] + ' - ' + dados['CEP'].apply(str) + ' ' + dados['CIDADE'] + ' ' + dados['UF']
			dados['latitude'] = dados['COORDENADAS'].apply(retorna_latitude)
			dados['longitude'] = dados['COORDENADAS'].apply(retorna_longitude)

			massa = dados[['tipo','data-ocorrencia','endereco','latitude','longitude']]
			massa.to_csv(SITE_PATH + FILE.format(CRIME, YEAR, smonth))

def wrangle_json_data(json):
	json = json.replace("u'","'")
	json = json.replace("M'Boi", 'M Boi')
	json = json.replace("D'Oeste", 'D Oeste')
	json = json.replace("d'agua", 'd agua')
	json = json.replace("d'xc1gua", 'd xc1gua')
	json = json.replace("d'\"xc1gua", 'd xc1gua')
	json = json.replace('D"aviz', 'D aviz')
	json = json.replace("D'aviz", 'D aviz')
	json = json.replace("D'Aviz", 'D Aviz')
	json = json.replace('D"Aviz', 'D Aviz')
	json = json.replace("D'abril", 'D abril')
	json = json.replace('D"abril', 'D abril')
	json = json.replace("Sant'Anna", "Sant Anna")
	json = json.replace("d'avila", "d avila")
	json = json.replace("D'Ascoli", "D Ascoli")
	json = json.replace('u"', '"')
	json = json.replace("'", '"')
	json = json.replace("\\","")
	json = json.replace("True",'"True"')

	return json

def retorna_latitude(json):
	if json and (type(json) == 'float' and not math.isnan(float(json))) and len(json) > 2:
		json = wrangle_json_data(json)

		geo_data = JSONDecoder().decode(json)
		return geo_data[0]['geometry']['location']['lat']

def retorna_longitude(json):
	if json and (type(json) == 'float' and not math.isnan(float(json))) and len(json) > 2:
		json = wrangle_json_data(json)
		
		geo_data = JSONDecoder().decode(json)
		return geo_data[0]['geometry']['location']['lng']

if __name__ == '__main__':
    gera_massa()
