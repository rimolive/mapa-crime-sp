import pandas as pd
from json import JSONDecoder

BASE_PATH = "" # Preencha esse valor com um caminho para gravar os arquivos csv.

YEAR = "2017"
MONTH = "05"
PATH = "{}/data/{}/".format(BASE_PATH, YEAR)
FILE = "homicidio_{}_{}.csv".format(YEAR, MONTH)
GEO_FILE = "homicidio_{}_{}_geo.csv".format(YEAR, MONTH)

def gera_massa():
	dados = pd.read_csv(PATH + GEO_FILE, na_values='', delimiter=',', header=0)
	massa = dados[dados['CIDADE'] == 'S.PAULO']
	massa['tipo'] = "Homicidio"
	massa['data-ocorrencia'] = dados['DATAOCORRENCIA']
	massa['endereco'] = dados['LOGRADOURO'] + ', ' + dados['NUMERO'].apply(str) + ' - ' + dados['CIDADE'] + ' ' + dados['UF']
	massa['latitude'] = dados['coord'].apply(retorna_latitude)
	massa['longitude'] = dados['coord'].apply(retorna_longitude)

	print type(massa)
	massa = massa[['tipo','data-ocorrencia','endereco','latitude','longitude']]
	massa.to_csv(PATH + 'massa.csv')

def retorna_latitude(json):
	if json and len(json) > 2:
		json = json.replace("u'","'")
		json = json.replace("M'Boi", 'M Boi')
		json = json.replace('u"', '"')
		json = json.replace("'", '"')
		json = json.replace("\\","")
		json = json.replace("True",'"True"')

		geo_data = JSONDecoder().decode(json)
		return geo_data[0]['geometry']['location']['lat']

def retorna_longitude(json):
	if json and len(json) > 2:
		json = json.replace("u'","'")
		json = json.replace("M'Boi", 'M Boi')
		json = json.replace('u"', '"')
		json = json.replace("'", '"')
		json = json.replace("\\","")
		json = json.replace("True",'"True"')

		geo_data = JSONDecoder().decode(json)
		return geo_data[0]['geometry']['location']['lng']

if __name__ == '__main__':
    gera_massa()
