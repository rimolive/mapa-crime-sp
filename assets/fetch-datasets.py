from scrapy.http import FormRequest
from scrapy.spiders import Spider

'''
Scrapy spider que captura dados de crime da SSP (Secretaria
de Seguranca Publica) do Estado de Sao Paulo.

Referencias:

https://stackoverflow.com/questions/28974838/crawling-through-pages-with-postback-data-javascript-python-scrapy
https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#std:setting-RETRY_ENABLED
'''

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

BASE_PATH = "" # Preencha esse valor com um caminho para gravar os arquivos xls.

class SegurancaPublicaSpider(Spider):
    name = 'ssp spider'
    start_urls = ['http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx']
    crimes = [
        'FurtoCelular'
        'FurtoVeiculo',
        'Homicicio'
        'Latrocinio',
        'LesaoMorte',
        'MortePolicial',
        'MorteSuspeita',
        'RouboCelular',
        'RouboVeiculo'
    ]
    download_delay = 1.5
    download_timeout = 1080
    years = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    def parse(self, response):
        for crime in self.crimes:
            yield FormRequest(
                self.start_urls[0],
                method='POST',
                formdata={
                    '__EVENTTARGET': "ctl00$cphBody$btn{}".format(crime),
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                },
                dont_filter=True,
                meta={'crime': crime},
                headers=HEADERS,
                callback=self.parse_years
            )

    def parse_years(self, response):
        for year in self.years:
            crime = response.meta.get('crime')
            yield FormRequest(
				self.start_urls[0],
                method='POST',
				formdata = {
					'__EVENTTARGET': 'ctl00$cphBody$lkAno' + year,
					'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
				},
                dont_filter=True,
                meta={'crime': crime, 'year': year},
                headers=HEADERS,
				callback=self.parse_months
			)

    def parse_months(self, response):
        for month in self.months:
            crime = response.meta.get('crime')
            year = response.meta.get('year')
            yield FormRequest(
				self.start_urls[0],
                method='POST',
				formdata = {
					'__EVENTTARGET': 'ctl00$cphBody$lkMes' + month,
					'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
				},
                dont_filter=True,
                meta={'crime': crime, 'year': year, 'month': month},
                headers=HEADERS,
				callback=self.parse_export
			)

    def parse_export(self, response):
        crime = response.meta.get('crime')
        year = response.meta.get('year')
        month = response.meta.get('month')
        yield FormRequest(
			self.start_urls[0],
            method='POST',
			formdata = {
				'__EVENTTARGET': 'ctl00$cphBody$ExportarBOLink',
				'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
			},
            dont_filter=True,
            meta={'crime': crime, 'year': year, 'month': month},
            headers=HEADERS,
			callback=self.parse_result
		)

    def parse_result(self, response):
        crime = response.meta.get('crime')
        year = format(int(response.meta.get('year')), '02d')
        month = format(int(response.meta.get('month')), '02d')
        filename = "{}/data/20{}/{}_20{}_{}.xls".format(BASE_PATH, year, crime, year, month)
        print("Writing file {} now!".format(filename))
        with open(filename, 'w+') as csv_file:
            csv_file.write(response.body)
            csv_file.close
