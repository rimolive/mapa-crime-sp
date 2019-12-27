#!/bin/bash

###################################
# Descobrir caractere hexa no vim: ga
# Substituir caractere hexa no vim: :%s/\%x<hex-value>//g
#######################################

BASE_PATH="`pwd`" # Preencha esse valor com um caminho para ler os arquivos xls e converter para csv.

declare -a crimes=(
	'Feminicidio'
	'FurtoCelular'
	'FurtoVeiculo'
	'Homicicio'
	'Latrocinio'
	'LesaoMorte'
	'MortePolicial'
	'MorteSuspeita'
	'RouboCelular'
	'RouboVeiculo'
);

declare -a years=(
	'2003'
	'2004'
	'2005'
	'2006'
	'2007'
	'2008'
	'2009'
	'2010'
	'2011'
	'2012'
	'2013'
	'2014'
	'2015'
	'2016'
	'2017'
	'2018'
	'2019'
);

for crime in ${crimes[@]}; do
	for year in ${years[@]}; do
		pushd raw/$year > /dev/null
		for month in `ls $crime\_* | tr '_' ' ' | tr '.' ' ' | awk '{print $3}'`; do

			if [ ! -d "../../wrangled/$year" ]; then
				mkdir -p ../../wrangled/$year
			fi

			lcrime=$(echo $crime | tr '[:upper:]' '[:lower:]')

			if [ -f $crime\_$year\_$month.xls ]; then
				cp -v $crime\_$year\_$month.xls ../../wrangled/$year/$lcrime\_$year\_$month.tsv

				pushd ../../wrangled/$year > /dev/null
				sed -i 's/\x00//g' $lcrime\_$year\_$month.tsv
				sed -i 's/\"//g' $lcrime\_$year\_$month.tsv
				cat $lcrime\_$year\_$month.tsv | tr '\t' ',' >  $lcrime\_$year\_$month.csv

				# Descobre o encoding atual do arquivo para assim converter para UTF-8
				ENCODING=$(file -i $lcrime\_$year\_$month.csv | cut -d ';' -f2 | cut -d '=' -f2 | tr '[:lower:]' '[:upper:]')
				iconv -f $ENCODING -t UTF-8 $lcrime\_$year\_$month.csv -o $lcrime\_$year\_$month.csv.converted

				# Efetua o processo de conversao para UTF-8, remove o arquivo antigo para ficar com o novo
				rm -rf $lcrime\_$year\_$month.csv
				mv $lcrime\_$year\_$month.csv.converted $lcrime\_$year\_$month.csv

				rm -rf $lcrime\_$year\_$month.tsv
				popd > /dev/null
			fi
		done
		popd > /dev/null
	done
done