import scrapy
import json
decoder = json.JSONDecoder()

#> tass_previews_href.json && scrapy runspider tass_2.py -o tass_previews_href.json

with open('tass_sections.json', 'r') as fp:
    list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []
list_urls.append('https://tass.ru')

for x in list_input:
	print x['href']
	string = 'https://tass.ru' + x['href']
	list_urls.append(string)

print list_urls

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = list_urls;

	def parse(self, response):
		#for quote in response.css('a.news-preview'):
		for quote in response.css('div.news-list__item a'):
			yield {
				#'title': quote.css('span.news-preview__title').get(),
				'href': quote.xpath('@href').get(),
				#'author': quote.xpath('span/small/text()').get(),
			}
		for quote in response.css('a.news-preview'):
			yield {
				#'title': quote.css('span.news-preview__title').get(),
				'href': quote.xpath('@href').get(),
				#'author': quote.xpath('span/small/text()').get(),
			}
