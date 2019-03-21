import scrapy
import json
decoder = json.JSONDecoder()

#> duma_previews_href.json && scrapy runspider duma_2.py -o duma_previews_href.json
# scrapy shell https://www.pnp.ru/federation-council/
# response.css('div.item div.title').xpath('a/@href').get()
a = '''
with open('rg_sections.json', 'r') as fp:
    list_input = json.load(fp)

print list_input
print len(list_input)
print list_input[0]['href']

list_urls = []
list_urls.append('https://rg.ru')

for x in list_input:
	print x['href']
	string = 'https://rg.ru' + x['href']
	list_urls.append(string)

print list_urls
'''
class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'http://duma.gov.ru/news/duma/',
		'http://duma.gov.ru/news/duma/page/2/',
	]

	def parse(self, response):
		#for quote in response.css('a.news-preview'):
		for quote in response.css('article.article--post'):
			yield {
				#'title': quote.css('span.news-preview__title').get(),
				'href': quote.xpath('a/@href').get(),
				#'author': quote.xpath('span/small/text()').get(),
			}
