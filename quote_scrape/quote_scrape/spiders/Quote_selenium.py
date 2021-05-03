import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from shutil import which


class QuoteSpiderSelenium(scrapy.Spider):
    name = 'Quote_selenium'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # chrome_path = which("chromedriver")
        driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
        driver.set_window_size(1920, 1080) # remember driver.set_window_size(width, length)
        driver.get("http://quotes.toscrape.com/js")

        self.html = driver.page_source
        driver.close()

    # script = '''
    #     function main(splash, args)
    #         assert(splash:go(args.url))
    #         assert(splash:wait(1)) 
    #         return splash:html()
    #     end
    # '''

    # def start_requests(self): 
    #     yield SplashRequest(url="http://quotes.toscrape.com/js/", callback=self.parse, endpoint="execute", args={
    #         "lua_source": self.script
    #     })

    def parse(self, response):
        resp = Selector(text=self.html)
        for quote in resp.xpath("//div[@class='quote']"):
            yield {
                'quote_text': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//span[2]/small[@class='author']/text()").get(),
                'tags': quote.xpath(".//div[@class='tags']/a/text()").getall()
            }