import scrapy
import json
decoder = json.JSONDecoder()

#> rg_previews_href.json && scrapy runspider rg_2.py -o rg_previews_href.json

with open('rg_sections.json', 'r') as fp:
    list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []
list_urls.append('https://rg.ru')

for x in list_input:
	print x['href']
	if(x['href']!='/tema/auto/' and x['href']!='/tema/digital/' and x['href']!='/tema/kino/'):
		string = 'https://rg.ru' + x['href']
		list_urls.append(string)

print list_urls

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = list_urls

	def parse(self, response):
		for quote in response.css('div.b-news__list-item h2.b-news__list-item-title'):
			yield {
				'href': quote.xpath('a/@href').get(),
			}
