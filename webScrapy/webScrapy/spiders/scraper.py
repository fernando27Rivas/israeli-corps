# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from webScrapy.items import WebscrapyItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['justice.gov.il']
    search_url = 'https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8'
    start_urls = ['https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8']
    
    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class, "k-pager-wrap")]/a/span[contains(@class, "k-icon")]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div/a/u')), callback='parse',
             follow=False),
    }


    def parse(self, response):
        print("I'm Here")

        url = "https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8"
        browser = webdriver.Firefox()
        browser.get(url)
        search_box = browser.find_element_by_id("CorporationName")
        search_box.send_keys("טבע")
        browser.find_element_by_xpath("//div/input[contains(@id, 'btnSearchSearchCorporation1')]").click()
        time.sleep(10)
        idCompany = browser.find_elements_by_xpath("//table/tbody/tr/td[2]")

        items = []
        i = 1
        j = 2
        while i < len(idCompany)*2:
            ml_item = WebscrapyItem()
            browser.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[1]").click()
            time.sleep(5)
            insideData= browser.find_elements_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col')]")

            ompany_id = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[2]").text
            ebrew_name = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[3]").text
            ml_item['company_id'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[2]").text
            ml_item['hebrew_name'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[3]").text
            ml_item['company_type'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[4]").text
            ml_item['company_status'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[5]").text
            ml_item['company_status2'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[6]").text
            ml_item['company_last_year_report'] = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[7]").text
            items.append(ml_item)
            i = i + 2
            j = j + 2

        print(items)
        print(insideData)

        #for idc in idCompany:
            #ml_item['company_id'] = idc.text
         #   print(idc.text)
        # links = browser.find_element_by_class_name('')
        # for link in links:
        #     print(link)

   # def start_requests(self):
    #    print("INSIDE SPLASH")
     #   yield SplashRequest(url="https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8", callback=self.parse1, endpoint='execute')
    
    # def parse(self, response):
    #     print("INSIDE LOGIN FBO")
    #     '''
    #     Generate a login form request.
    #     '''
    #
    #     p1 = response.css("input[name=UnitsType] ::attr(value)").extract_first()
    #     p2 = response.css("input[name=CorporationType] ::attr(value)").extract_first()
    #     p3 = response.css("input[name=ContactType] ::attr(value)").extract_first()
    #     p4 = response.css("input[name=CorporationNameDisplayed] ::attr(value)").extract_first()
    #     p5 = response.css("input[name=CorporationNumberDisplayed] ::attr(value)").extract_first()
    #     p11 = response.css("input[name=CorporationNameDisplayed] ::attr(value)").extract_first()
    #     p6 = response.css("input[name=currentJSFunction] ::attr(value)").extract_first()
    #     p7 = response.css("input[name=RateExposeDocuments] ::attr(value)").extract_first()
    #     p8 = response.css("input[name=TollCodeExposeDocuments] ::attr(value)").extract_first()
    #     p9 = response.css("input[name=RateCompanyExtract] ::attr(value)").extract_first()
    #     p10 = response.css("input[name=RateYearlyToll] ::attr(value)").extract_first()
    #
    #     data = {
    #         'UnitsType': p1,
    #         'CorporationType': p2,
    #         'ContactType': p3,
    #         'CorporationNameDisplayed': p4,
    #         'CorporationNumberDisplayed': p5,
    #         'CorporationName': 'טבע',
    #         'CorporationNumber': '',
    #         'currentJSFunction': 'Process.SearchCorporation.Search()',
    #         'RateExposeDocuments': p7,
    #         'TollCodeExposeDocuments': p8,
    #         'RateCompanyExtract': p9,
    #         'RateYearlyToll': p10,
    #     }
    #     yield SplashRequest(url="https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8", endpoint='execute', args=data, callback=self.parse1)

    # def parse1(self, response):
    #     ml_item = WebscrapyItem()
    #     print("I'm here")
    #     ml_item['id'] = response.xpath('//div/a/u').extract()
    #     print(ml_item['id'])