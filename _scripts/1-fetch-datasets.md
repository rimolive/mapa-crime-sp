---
title: fetch-datasets.py
labels:
- Scrapping
- Scrapy
---

Esse script é um spider escrito em Python e utilizando a biblioteca
 [Scrapy](https://scrapy.org/). Nele, é possível capturar todas as 
 informações do site da SSP em formato excel (.xls). Para executar
 o script, instale o scrapy:

 ```
 $ pip install -u scrapy
 ```

 E depois execute o scrapy passando esse script como entrada:

 ```
 $ scrapy runspider fetch-datasets.py
 ```