import scrapy

# > pnp_sections.json &&	 scrapy runspider pnp_1.py -o pnp_sections.json

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'https://www.pnp.ru/',
	]

	def parse(self, response):
		for quote in response.css('div.menu_top a[href*="pnp.ru"]'):
			yield {
				'href': quote.xpath('@href').get(),
			}

