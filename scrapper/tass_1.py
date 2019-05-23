import scrapy

# > tass_sections.json &&	scrapy runspider tass_1.py -o tass_sections.json

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'https://tass.ru/',
	]

	def parse(self, response):
		for quote in response.css('a.menu-sections-list__title'):
			yield {
				'href': quote.xpath('@href').get(),
			}

