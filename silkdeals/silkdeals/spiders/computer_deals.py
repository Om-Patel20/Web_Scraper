import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapy_selenium import SeleniumRequest


class ComputerDealsSpider(scrapy.Spider):
    name = 'computer_deals'
    allowed_domains = ['slickdeals.net/computer-deals']
    start_urls = ['http://slickdeals.net/computer-deals/']

    def __init__(self, link="https://slickdeals.net/computer-deals/"):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(link)
        self.html = driver.page_source
        driver.close()
    
    def parse(self, response):
        resp = Selector(text=self.html) # selenium scrapy response
        products = resp.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            yield {
                'name': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/text()").get(),
                'link': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get(),
                'store_name': product.xpath("normalize-space(.//*[contains(@class, 'itemStore')]/text())").get(),
                'price': product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }
        
        next_page = resp.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"http://slickdeals.net/computer-deals{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )

            # Big Doubt: - How to do pagination using selenium webdriver