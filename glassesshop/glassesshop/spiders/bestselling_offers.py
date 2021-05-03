import scrapy


class BestsellingOffersSpider(scrapy.Spider):
    name = 'bestselling_offers'
    allowed_domains = ['www.glassesshop.com']
    #start_urls = ['https://www.glassesshop.com/bestsellers'] /Because we have used the start_requests() function, we don't need this list

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'
        })

    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div"):
            yield {
                'product_url': product.xpath(".//div[4]/div[2]/div/div[1]/div/a/@href").get(),
                'image_url': product.xpath(".//div[3]/a/img[2]/@data-src").get(),
                'product_name': product.xpath(".//div[4]/div[2]/div/div[1]/div/a/text()").get(),
                'product_price': product.xpath(".//div[4]/div[2]/div/div[2]/div/div/span/text()").get(),
                'user_agent': response.request.headers['User-Agent']
            }
        
        next_page = response.xpath("//a[@class='page-link' and @rel='next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'
            })