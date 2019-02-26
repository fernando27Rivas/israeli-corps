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
from webScrapy import settings


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

        list = settings.LIST

        for listelement in list:

            browser = webdriver.Firefox()
            browser.get(url)
            search_box = browser.find_element_by_id("CorporationName")
            search_box.send_keys(listelement)
            browser.find_element_by_xpath("//div/input[contains(@id, 'btnSearchSearchCorporation1')]").click()
            time.sleep(10)
            
            rests = browser.find_elements_by_xpath("//table/tbody/tr/td[2]")
            next = None
            if len(rests) < 1:
                next = 1

            while next is None:


                idCompany = browser.find_elements_by_xpath("//table/tbody/tr/td[2]")


                i = 1
                j = 2
                while i < len(idCompany)*2:


                    try:

                        browser.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[1]").click()
                        time.sleep(5)
                        ompany_id = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[2]").text
                        ebrew_name = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[3]").text
                        ompany_type = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[4]").text
                        ompany_status = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[5]").text
                        ompany_status2 = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[6]").text
                        ompany_last_year_report = browser.find_element_by_xpath("//table/tbody/tr[" + str(i) + "]/td[7]").text


                        nglish_name = browser.find_element_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col-sm-3')]/span").text
                        ompany_start_date = browser.find_element_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col-sm-7')]/span[contains(@id, 'RegistrationDate')]").text
                        escs = browser.find_elements_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col-sm-7')]/span[not(contains(@id, 'RegistrationDate'))]")
                        ompany_desc = escs[0].text
                        ompany_desc_2 = escs[1].text
                        imitslist = browser.find_elements_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col-sm-1')][not(contains(@class, 'moj-bold'))]/span")
                        ompany_limit = imitslist[1].text
                        ompany_task = browser.find_element_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div/div[contains(@class, 'col-sm-1')][contains(@id, 'tollYearly')]").text
                        lists = browser.find_elements_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/h3")
                        izeH3 = len(lists)
                        if izeH3 == 2:
                            ompany_info = lists[1].text
                        if izeH3 == 3:
                            ompany_info = lists[2].text
                        addres = browser.find_element_by_xpath("//table/tbody/tr[" + str(j) + "]/td/div/div[9]").text


                        with open('data.csv', 'a') as csvFile:
                            data_writer = csv.writer(csvFile)
                            data_writer.writerow([ompany_id, ebrew_name, ompany_type, ompany_status, ompany_status2, ompany_last_year_report, nglish_name, ompany_start_date, ompany_desc, ompany_desc_2, ompany_limit, ompany_task, addres, ompany_info])


                        i = i + 2
                        j = j + 2

                    except:
                        pass
                try:
                    salto = browser.find_element_by_xpath("//div/a[contains(@class, 'k-link')][not(contains(@class, 'k-state-disabled'))][contains(@title, 'לעמוד הבא')]")
                    salto.click()
                except:
                        next = 1

            browser.close()




