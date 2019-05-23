import scrapy
import json
decoder = json.JSONDecoder()

#> pnp_previews_href.json && scrapy runspider pnp_2.py -o pnp_previews_href.json

with open('pnp_sections.json', 'r') as fp:
    list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []
list_urls.append('https://www.pnp.ru')

for x in list_input:
	print x['href']
	string = x['href']
	list_urls.append(string)

print list_urls

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = list_urls

	def parse(self, response):
		for quote in response.css('div.item div.title'):
			yield {
				'href': quote.xpath('a/@href').get(),
			}
