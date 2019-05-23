import scrapy
import json
decoder = json.JSONDecoder()

# > tass_page_data.json && scrapy runspider tass_3.py -o tass_page_data.json

with open('tass_previews_href.json', 'r') as fp:
	list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []

for x in list_input:
	print x['href']
	string = 'https://tass.ru' + x['href']
	list_urls.append(string)

list(set(list_urls))
print list_urls

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = list_urls

	def parse(self, response):
		yield {
			'title': response.xpath('//meta[@property=$val]/@content', val='og:title').get(),
			'href': response.xpath('//meta[@property=$val]/@content', val='og:url').get(),
			'image': response.xpath('//meta[@property=$val]/@content', val='og:image').get(),
			'description': response.xpath('//meta[@property=$val]/@content', val='og:description').get(),
			'text': response.css('div.text-content').get()
		}
