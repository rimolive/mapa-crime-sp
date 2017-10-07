#!/bin/bash

###################################
# Descobrir caractere hexa no vim: ga
# substituir caractere hexa no vim: :%s/\%x<hex-value>//g
#######################################

BASE_PATH="`pwd`" # Preencha esse valor com um caminho para ler os arquivos xls e converter para csv.

declare -a crimes=(
	'FurtoCelular'
	'FurtoVeiculo'
	'Homicicio'
	'Latrocinio'
	'LesaoMorte'
	'MortePolicial'
	#'MorteSuspeita'
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
);

for crime in ${crimes[@]}; do
	for year in ${years[@]}; do
		pushd raw/$year > /dev/null
		for month in `ls $crime\_* | tr '_' ' ' | tr '.' ' ' | awk '{print $3}'`; do

			if [ ! -d "../../wrangled/$year" ]; then
				mkdir -p ../../wrangled/$year
			fi

			lcrime=$(echo $crime | tr '[:upper:]' '[:lower:]')

			cp -v $crime\_$year\_$month.xls ../../wrangled/$year/$lcrime\_$year\_$month.tsv

			pushd ../../wrangled/$year > /dev/null
			sed -i 's/\x00//g' $lcrime\_$year\_$month.tsv
			sed -i 's/,//g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc7/C/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xfa/u/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xed/i/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xf7/o/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xf4/o/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xe3/a/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc3/A/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc1/A/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc2/A/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xcd/I/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xe0/a/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xe9/e/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc9/E/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xca/E/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xea/e/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xc9/E/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xd3/O/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xd4/O/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xd5/O/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xda/U/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xaa/a./g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xe7/c/g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xa7/par. /g' $lcrime\_$year\_$month.tsv
			sed -i 's/\xba/o./g' $lcrime\_$year\_$month.tsv
			sed -i 's/\"//g' $lcrime\_$year\_$month.tsv
			cat $lcrime\_$year\_$month.tsv | tr '\t' ',' >  $lcrime\_$year\_$month.csv
			rm -rf $lcrime\_$year\_$month.tsv
			popd > /dev/null
		done
		popd > /dev/null
	done
done