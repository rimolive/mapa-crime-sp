import requests
from urllib import urlopen
from urllib import urlencode
from bs4 import BeautifulSoup

'''

'''
BASE_PATH = "" # Preencha esse valor com um caminho para gravar os arquivos xls.

url = 'http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx'

commands = ['Homicicio']
			'FurtoVeiculo',
			'RouboCelular',
			'Latrocinio',
			'MortePolicial',
			'RouboVeiculo',
			'LesaoMorte',
			'MorteSuspeita',
			'FurtoCelular']

years = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
path = '{}/raw/'.format(BASE_PATH)

html = urlopen(url)
bsObj = BeautifulSoup(html.read(), "lxml")

view_state =  bsObj.find_all('input')[0]['value']
event_validation =  bsObj.find_all('input')[1]['value']

def request_year(url, view_state, event_validation):
	for year in years:
		year_params = {
			'__EVENTTARGET': 'ctl00$cphBody$lkAno' + year,
			'__VIEWSTATE': view_state,
	 		'__EVENTVALIDATION': event_validation
		}
		response_year = urlopen(url, urlencode(year_params))

		if response_year.getcode() == 200:
			bsObj = BeautifulSoup(response_year.read(), "lxml")
			view =  bsObj.find_all('input')[0]['value']
			event =  bsObj.find_all('input')[1]['value']
			request_month(url, view, event, year)
		else:
			print "Year request returned {}. {}".format(response_year.getcode(), response_year.read())

def request_month(url, view_state, event_validation, year):
	for month in months:
		year_params = {
			'__EVENTTARGET': 'ctl00$cphBody$lkMes' + month,
			'__VIEWSTATE': view_state,
			'__EVENTVALIDATION': event_validation
		}
		response_month = urlopen(url, urlencode(year_params))
		if response_month.getcode() == 200:
			export_to_xls(url, view_state, event_validation, year, month)
		else:
			print "Month request returned {}. {}".format(response_month.getcode(), response_month.read())

def export_to_xls(url, view_state, event_validation, year, month):
	export_params = {
		'__EVENTTARGET': 'ctl00$cphBody$ExportarBOLink',
		'__VIEWSTATE': view_state,
		'__EVENTVALIDATION': event_validation
	}
	content = urlopen(url, urlencode(export_params))

	filename = "{}20{}/{}_20{}_{}.xls".format(path,
												  format(int(year), '02d'),
												  command,
												  format(int(year), '02d'),
												  format(int(month), '02d'))
	try:
		with open(filename) as xls_file:
			xls_file.write(content.read())
			xls_file.close()
	except:
		print "Can't write file {}".format(filename)
		print content.read()



for command in commands:
	command_params = {
 		'__EVENTTARGET': 'ctl00$cphBody$btn' + command,
 		'__VIEWSTATE': view_state,
		'__EVENTVALIDATION': event_validation
 	}
	response_command = urlopen(url, urlencode(command_params))
	
	if response_command.getcode() == 200:
		request_year(url, view_state, event_validation)	
	else:
		print "Command request returned {}. {}".format(response_command.getcode(), response_command.read())
	