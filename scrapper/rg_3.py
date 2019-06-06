import scrapy
from urlparse import urlparse
import json
decoder = json.JSONDecoder()

# > rg_page_data.json && scrapy runspider rg_3.py -o rg_page_data.json

with open('rg_previews_href.json', 'r') as fp:
	list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []

for x in list_input:
	print x['href']
	string = 'https://rg.ru' + x['href']
	list_urls.append(string)

list(set(list_urls))
print list_urls

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = list_urls

	def parse(self, response):
		#url_parsed = urlparse(response.xpath('//meta[@property=$val]/@content', val='og:url').get())
		#path =  url_parsed.path
		#int_a = path.find('/')
		#int_a = int_a + 1
		#int_b = path.find('/',int_a)
		#print path[int_a:int_b]
		yield {
			'title': response.xpath('//meta[@property=$val]/@content', val='og:title').get(),
			'href': response.xpath('//meta[@property=$val]/@content', val='og:url').get(),
			'image': response.xpath('//meta[@property=$val]/@content', val='og:image').get(),
			'description': response.xpath('//meta[@property=$val]/@content', val='og:description').get(),
			'text': response.css('div.b-material-wrapper__text p').getall(),
			#'section': path[int_a:int_b]  #rg.ru stores the date, not the section, will get used as testing material.
			'section': ''  
		}

#response.xpath('//meta[@property=$val]/@content', val='og:title').get()
