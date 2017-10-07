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
        for year in range(2003,2009):
        for month in range(1,12):
            smonth = format(month, '02d')
            filename = BASE_PATH + FILE.format(year, crime, year, smonth)
            print "Normalizing file {}...".format(filename)
            dados = pd.read_csv(filename, na_values='', delimiter=',', header=0)

            if 'LATITUDE' not in dados:
                dados['LATITUDE'] = ''
            if 'LONGITUDE' not in dados:
                dados['LONGITUDE'] = ''

            if 'ID_CIRCUNSCRICAO' in dados:
                dados = dados.drop("ID_CIRCUNSCRICAO", axis=1)
            if 'HISTORICO_BO' in dados:
                dados = dados.drop("HISTORICO_BO", axis=1)

            dados.to_csv(BASE_PATH + FILE.format(year, crime, year, smonth), index=False)

if __name__ == '__main__':
    normalize()