import scrapy
import json
decoder = json.JSONDecoder()

#> duma_previews_href.json && scrapy runspider duma_2.py -o duma_previews_href.json
class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'http://duma.gov.ru/news/duma/',
		'http://duma.gov.ru/news/duma/page/2/',
	]

	def parse(self, response):
		for quote in response.css('article.article--post'):
			yield {
				'href': quote.xpath('a/@href').get(),
			}
