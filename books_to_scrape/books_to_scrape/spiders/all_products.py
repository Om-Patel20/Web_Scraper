import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AllProductsSpider(CrawlSpider):
    name = 'all_products'
    allowed_domains = ['books.toscrape.com']
    #start_urls = ['http://books.toscrape.com/']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='image_container']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), follow=True, process_request='set_user_agent')
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'book_name': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'user-agent': response.request.headers['User-Agent']
        }
