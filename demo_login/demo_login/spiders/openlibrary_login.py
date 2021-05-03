import scrapy
from scrapy import FormRequest


class OpenlibraryLoginSpider(scrapy.Spider):
    name = 'openlibrary_login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid='register',
            formdata={
                'username': 'timmoby25@gmail.com',
                'password': 'brainpop',
                'redirect': 'https://openlibrary.org/',
                'debug_token': '',
                'login': 'Log In'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # if response.xpath("").get():
        print('Logged in...')