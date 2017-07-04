import scrapy

'''
Scrapy spider que captura dados de crime da SSP (Secretaria
de Seguranca Publica) do Estado de Sao Paulo.
'''
class SegurancaPublicaSpider(scrapy.Spider):
    BASE_PATH = "" # Preencha esse valor com um caminho para gravar os arquivos xls.
    name = 'ssp spider'
    start_urls = ['http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx']
    commands = ['ctl00$cphBody$btnHomicicio'
                'ctl00$cphBody$btnFurtoVeiculo',
                'ctl00$cphBody$btnRouboCelular',
                'ctl00$cphBody$btnLatrocinio',
                'ctl00$cphBody$btnMortePolicial',
                'ctl00$cphBody$btnRouboVeiculo',
                'ctl00$cphBody$btnLesaoMorte',
                'ctl00$cphBody$btnMorteSuspeita',
                'ctl00$cphBody$btnFurtoCelular'
        ]
    download_delay = 1.5
    years = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    counter = 0

    def parse(self, response):
        for command in self.commands:
            yield scrapy.FormRequest(
                self.start_urls[0],
                formdata={
                    '__EVENTTARGET': command,
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                },
                callback=self.parse_years
            )



    def parse_years(self, response):
		for year in self.years:
			yield scrapy.FormRequest(
				self.start_urls[0],
				formdata = {
					'__EVENTTARGET': 'ctl00$cphBody$lkAno' + year,
					'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
				},
				callback=self.parse_months
			)

    def parse_months(self, response):
		for month in self.months:
			yield scrapy.FormRequest(
				self.start_urls[0],
				formdata = {
					'__EVENTTARGET': 'ctl00$cphBody$lkMes' + month,
					'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
				},
				callback=self.parse_export
			)

    def parse_export(self, response):
		yield scrapy.FormRequest(
			self.start_urls[0],
			formdata = {
				'__EVENTTARGET': 'ctl00$cphBody$ExportarBOLink',
				'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
			},
			callback=self.parse_result
		)

    def parse_result(self, response):
        self.counter += 1
        filename = '{}/raw/' + str(self.BASE_PATH, self.counter) + '.xls'
        print("Writing file {} now!".format(filename))
        with open(filename, 'w+') as csv_file:
            csv_file.write(response.body)
            csv_file.close


