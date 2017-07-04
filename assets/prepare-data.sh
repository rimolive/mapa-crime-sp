#!/bin/bash

declare -a years=('2003'
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
				  '2017');

BASE_PATH="" # Preencha esse valor com um caminho para ler os arquivos xls e converter para csv.

for year in ${years[@]}; do
	pushd $BASE_PATH/raw/$year > /dev/null
	for month in `ls | tr '_' ' ' | tr '.' ' ' | awk '{print $3}'`; do

		if [ ! -d "$BASE_PATH/data/$year" ]; then
			mkdir -p $BASE_PATH/data/$year
		fi

		cp -v Homicidio_$year\_$month.xls $BASE_PATH/data/$year/homicidio_$year\_$month.tsv

		pushd $BASE_PATH/data/$year > /dev/null
		sed -i 's/\x00//g' homicidio_$year\_$month.tsv
		sed -i 's/,//g' homicidio_$year\_$month.tsv
		sed -i 's/\xc7/C/g' homicidio_$year\_$month.tsv
		sed -i 's/\xfa/u/g' homicidio_$year\_$month.tsv
		sed -i 's/\xed/i/g' homicidio_$year\_$month.tsv
		sed -i 's/\xf7/o/g' homicidio_$year\_$month.tsv
		sed -i 's/\xe3/a/g' homicidio_$year\_$month.tsv
		sed -i 's/\xc3/A/g' homicidio_$year\_$month.tsv
		sed -i 's/\xc1/A/g' homicidio_$year\_$month.tsv
		sed -i 's/\xc2/A/g' homicidio_$year\_$month.tsv
		sed -i 's/\xcd/I/g' homicidio_$year\_$month.tsv
		sed -i 's/\xe0/a/g' homicidio_$year\_$month.tsv
		sed -i 's/\xe9/e/g' homicidio_$year\_$month.tsv
		sed -i 's/\xc9/E/g' homicidio_$year\_$month.tsv
		sed -i 's/\xea/e/g' homicidio_$year\_$month.tsv
		sed -i 's/\xc9/E/g' homicidio_$year\_$month.tsv
		sed -i 's/\xd4/O/g' homicidio_$year\_$month.tsv
		sed -i 's/\xd3/O/g' homicidio_$year\_$month.tsv
		sed -i 's/\xaa/a./g' homicidio_$year\_$month.tsv
		sed -i 's/\xe7/c/g' homicidio_$year\_$month.tsv
		sed -i 's/\xa7/par. /g' homicidio_$year\_$month.tsv
		sed -i 's/\xba/o./g' homicidio_$year\_$month.tsv
		cat homicidio_$year\_$month.tsv | tr '\t' ',' >  homicidio_$year\_$month.csv
		rm -rf homicidio_$year\_$month.tsv
		popd > /dev/null
	done
	popd > /dev/null

done