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
				#'title': quote.css('span.news-preview__title').get(),
				'href': quote.xpath('@href').get(),
				#'author': quote.xpath('span/small/text()').get(),
			}


        #next_page = response.css('li.next a::attr("href")').get()
        #if next_page is not None:
        # yield response.follow(next_page, self.parse)

#>>> response.css('a.menu-sections-list__title::attr(href)').getall()
#[u'/v-strane', u'/politika', u'/nacionalnye-proekty', u'/mezhdunarodnaya-panorama', u'/ekonomika', u'/nedvizhimost', u'/msp', u'/armiya-i-opk', u'/obschestvo', u'/proisshestviya', u'/sport', u'/kultura', u'/nauka', u'/kosmos', u'/moskva', u'/moskovskaya-oblast', u'/spb-news', u'/ural-news', u'/sibir-news']
 ########
#		'https://tass.ru/nacionalnye-proekty',
#		'https://tass.ru/ekonomika',
#		'https://tass.ru/armiya-i-opk',
#		'https://tass.ru/mezhdunarodnaya-panorama',
##################