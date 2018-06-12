library(tidyverse)
library(jsonlite)

setwd("/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp")

data <- mescla_datasets('wrangled', 'furtoveiculo', 2005, get_months(4, 4))

# Remove NUMERO_BOLETIM. Motivo: O campo é identico aos campos ANO_BO e NUM_BO
data <- data %>%
  select(-NUMERO_BOLETIM)

# Converte BO_INICIADO para data/hora
data$BO_INICIADO <- as.POSIXct(strptime(data$BO_INICIADO, format="%d/%m/%Y %H:%M:%S"))

# Converte BO_EMITIDO para data/hora
data$BO_EMITIDO <- as.POSIXct(strptime(data$BO_EMITIDO, format="%d/%m/%Y %H:%M:%S"))

# Converte DATAOCORRENCIA para data
data$DATAOCORRENCIA <- as.POSIXct(strptime(data$DATAOCORRENCIA, format="%d/%m/%Y"))

# Converte PERIODOOCORRENCIA para Factor
data$PERIDOOCORRENCIA <- as.factor(data$PERIDOOCORRENCIA)

# Converte DATACOMUNICACAO para data
data$DATACOMUNICACAO <- as.POSIXct(strptime(data$DATACOMUNICACAO, format="%d/%m/%Y"))

# Converte DATAELABORACAO para data/hora
data$DATAELABORACAO <- as.POSIXct(strptime(data$DATAELABORACAO, format="%d/%m/%Y %H:%M:%S"))

# Converte BO_AUTORIA para Factor
data$BO_AUTORIA <- as.factor(data$BO_AUTORIA)

# Converte FLAGRANTE para Factor
data$FLAGRANTE <- as.factor(data$FLAGRANTE)

# Converte os valores de NUMERO_BOLETIM_PRINCIPAL vazios para NA
data$NUMERO_BOLETIM_PRINCIPAL <- sub("^$", NA, data$NUMERO_BOLETIM_PRINCIPAL)

# Transforma o texto do campo LOGRADOURO para deixar a informação homogenea. TODO mais coisas para fazer.
data$LOGRADOURO <- sub("^R ", "RUA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^R\\. ", "RUA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^R\\.", "RUA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^RUA\\: ", "RUA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AL ", "ALAMEDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AL\\. ", "ALAMEDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AL\\.", "ALAMEDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AV ", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AV\\. ", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AV\\.", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AV\\: ", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AV\\:", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^AVENIDA \\.", "AVENIDA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^PC ", "PRACA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^EST ", "ESTRADA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^ESTR. ", "ESTRADA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^TV ", "TRAVESSA ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" DR ", " DOUTOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" DR\\. ", " DOUTOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" CAP ", " CAPITAO ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" ALM ", " ALMIRANTE ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" PROF ", " PROFESSOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" ENG ", " ENGENHEIRO ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" GAL ", " GENERAL ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" GAL. ", " GENERAL ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" CEL ", " CORONEL ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" GOV ", " GOVERNADOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" SARG ", " SARGENTO ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" MAL ", " MARECHAL ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" VL. ", " VILA ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" DESEM ", " DESEMBARGADOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" SEN ", " SENADOR ", data$LOGRADOURO)
data$LOGRADOURO <- sub(" PRES ", " PRESIDENTE ", data$LOGRADOURO)
data$LOGRADOURO <- sub("^VIA ", "RODOVIA ", data$LOGRADOURO)
data$LOGRADOURO <- sub("S\\/N", "", data$LOGRADOURO)

data$LOGRADOURO <- sub("^ARAGARCAS", "RUA ARAGARCAS", data$LOGRADOURO)
data$LOGRADOURO <- sub("^ANITA TAGLIAFERRE", "RUA ANITA TAGLIAFERRE", data$LOGRADOURO)

# Remove os zeros do campo NUMERO
data$NUMERO[data$NUMERO == 0] <- NA

# Converte os valores de BAIRRO vazios para NA. TODO Mais coisas para fazer
data$BAIRRO <- sub("^$", NA, data$BAIRRO)

# Remove zeros do campo CEP
data$CEP <- str_trim(data$CEP)
data$CEP[data$CEP == 0] <- NA
data$CEP[data$CEP == 1] <- NA
data$CEP <- sub("-", "", data$CEP)
data$CEP <- sub("^GR\\.07", "", data$CEP)
data$CEP <- sub("^00$", "", data$CEP)
data$CEP <- sub("^$", NA, data$CEP)

# Trata o campo CIDADE, mudando as abreviacoes
data$CIDADE <- sub("^S\\.", "SAO ", data$CIDADE)
data$CIDADE <- sub("^SP$", "SAO PAULO", data$CIDADE)

# Trata os dados de DESCRICAOLOCAL para correcao de dados em branco e erros de codificacao
data$DESCRICAOLOCAL <- sub("^$", NA, data$DESCRICAOLOCAL)
data$DESCRICAOLOCAL <- sub("^Escrit\\\xf3rio$", "Escritorio", data$DESCRICAOLOCAL)
data$DESCRICAOLOCAL <- sub("^Estabelecimento banc\\\xe1rio$", "Estabelecimento bancario", data$DESCRICAOLOCAL)

# Converte os valores de EXAME vazios para NA.
data$EXAME <- sub("^$", NA, data$EXAME)

# Trata os dados de SOLUCAO para correcao de dados em branco e erros de codificacao
data$SOLUCAO <- sub("^$", NA, data$SOLUCAO)

# Trata os dados de DESDOBRAMENTO para correcao de dados em branco e erros de codificacao
data$DESDOBRAMENTO <- sub("^$", NA, data$DESDOBRAMENTO)

# Trata os dados de STATUS para correcao de dados em branco e erros de codificacao
data$STATUS <- sub("^$", NA, data$STATUS)

# Limpa os dados do campo COORDENADAS
data$COORDENADAS <- str_trim(data$COORDENADAS)
data$COORDENADAS <- sub("\\[\\]", NA, data$COORDENADAS)
data$COORDENADAS <- sub("^$", NA, data$COORDENADAS)

# Remove zeros do campo ANO_FABRICACAO
data$ANO_FABRICACAO[data$ANO_FABRICACAO == 0] <- NA

# Remove zeros do campo ANO_MODELO
data$ANO_MODELO[data$ANO_MODELO == 0] <- NA

# Remove ENDERECOCOMPLETO Motivo: O campo foi gerado para pesquisa de coordenadas
data <- data %>%
  select(-ENDERECOCOMPLETO)


write.csv(data,
          "/run/media/rmartine/TOSHIBA EXT/big-data-projects/ssp/wrangled/2005/furtoveiculo_2005_03.csv",
          row.names = FALSE,
          na = "")

## [WIP] A linha a seguir mostra a quantidade de crimes tratados por DP.
#data %>%
#  group_by(DELEGACIA_CIRCUNSCRICAO) %>%
#  summarise(crimes = n()) %>%
#  arrange(desc(crimes))

## [WIP] As linhas a seguir tratam o JSON de retorno do Geocoding.
#json_text <- "[{u'geometry': {u'location': {u'lat': -23.457825, u'lng': -47.4716057}, u'viewport': {u'northeast': {u'lat': -23.4564760197085, u'lng': -47.4702567197085}, u'southwest': {u'lat': -23.4591739802915, u'lng': -47.4729546802915}}, u'location_type': u'ROOFTOP'}, u'formatted_address': u'R. Jos\xe9 Lamberti, 213 - Jardim Santo Andre, Sorocaba - SP, 18077301, Brazil', u'place_id': u'ChIJGSawrw31xZQRtyK5nVNCg3I', u'address_components': [{u'long_name': u'213', u'types': [u'street_number'], u'short_name': u'213'}, {u'long_name': u'Rua Jos\xe9 Lamberti', u'types': [u'route'], u'short_name': u'R. Jos\xe9 Lamberti'}, {u'long_name': u'Jardim Santo Andre', u'types': [u'political', u'sublocality', u'sublocality_level_1'], u'short_name': u'Jardim Santo Andre'}, {u'long_name': u'Sorocaba', u'types': [u'administrative_area_level_2', u'political'], u'short_name': u'Sorocaba'}, {u'long_name': u'S\xe3o Paulo', u'types': [u'administrative_area_level_1', u'political'], u'short_name': u'SP'}, {u'long_name': u'Brazil', u'types': [u'country', u'political'], u'short_name': u'BR'}, {u'long_name': u'18077301', u'types': [u'postal_code'], u'short_name': u'18077301'}], u'partial_match': True, u'types': [u'street_address']}]"
#json_text <- stri_encode(json_text, from = "latin1", to = "ASCII")
#json_text <- gsub("[u]?\\'", '"', json_text)
#json_text <- gsub("\\[", '', json_text)
#json_text <- gsub("\\]", '', json_text)
#fromJSON(json_text)
