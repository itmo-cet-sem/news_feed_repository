import scrapy

# > rg_sections.json &&	 scrapy runspider rg_1.py -o rg_sections.json

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'https://rg.ru/',
	]

	def parse(self, response):
		for quote in response.css('div.b-categories__item a.b-link:not([href*=".html"])'):
			yield {
				'href': quote.xpath('@href').get(),
			}

