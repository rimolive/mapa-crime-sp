import pandas as pd

BASE_PATH = "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/database/"
FILE = "{}/{}_{}_{}.csv"

crimes = [
    'furtocelular',
    'furtoveiculo',
    'homicicio',
    'latrocinio',
    'lesaomorte',
    'mortepolicial',
    'roubocelular',
    'rouboveiculo'
]

def normalize():
    for crime in crimes:
        for year in range(2003,2017):
        for month in range(1,12):
            smonth = format(month, '02d')
            dados = pd.read_csv(BASE_PATH + FILE.format(year, crime, year, smonth), na_values='', delimiter=',', header=0)
            if 'LATITUDE' not in dados:
                dados['LATITUDE'] = ''
            if 'LONGITUDE' not in dados:
                dados['LONGITUDE'] = ''

            dados.to_csv(BASE_PATH + FILE.format(year, crime, year, smonth))

if __name__ == '__main__':
    normalize()