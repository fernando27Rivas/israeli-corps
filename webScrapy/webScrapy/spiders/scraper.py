# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from webScrapy.items import WebscrapyItem
from scrapy.http import Request, FormRequest


class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['https://ica.justice.gov.il']
    start_urls = ['https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8']
    
    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class, "k-pager-wrap")]/a/span[contains(@class, "k-icon")]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div/a/u')), callback='parse',
             follow=False),
    }
    
    def login(self, response):
        print("INSIDE LOGIN FBO")
        '''
        Generate a login form request.
        '''

        return FormRequest.from_response(response,
                                         formdata={
                                             'UnitsType': '8',
                                             'CorporationType': '3',
                                             'ContactType': '3',
                                             'CorporationNameDisplayed': 'no',
                                             'CorporationNumberDisplayed': '0',
                                             'CorporationName': 'טבע',
                                             'CorporationNumber': '',
                                             'currentJSFunction': 'Process.SearchCorporation.Search()',
                                             'RateExposeDocuments': '33.00',
                                             'TollCodeExposeDocuments': '129',
                                             'RateCompanyExtract': '10.00',
                                             'RateYearlyToll': '1133.00',
                                         },
                                         callback=self.parse)
    
    def parse(self, response):
        ml_item = WebscrapyItem()
        print("I'm here")
        ml_item['id'] = response.xpath('//p').extract()
        print(ml_item['id'])
