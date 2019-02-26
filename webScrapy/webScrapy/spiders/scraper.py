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
################################################################
import re, csv
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  

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
            
            
  

def write_stat(loops, time):
	with open('stat.csv', 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([loops, time])  	 
	
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
	
def wait_between(a,b):
	rand=uniform(a, b) 
	sleep(rand)
 
def dimention(driver): 
	d = int(driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table').get_attribute("class")[-1]);
	return d if d else 3  # dimention is 3 by default
	
# ***** main procedure to identify and submit picture solution	
def solve_images(driver):	
	WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"rc-imageselect-target"))
        ) 		
	dim = dimention(driver)	
	# ****************** check if there is a clicked tile ******************
	if check_exists_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr/td[@class="rc-imageselect-tileselected"]'):
		rand2 = 0
	else:  
		rand2 = 1 

	# wait before click on tiles 	
	wait_between(0.5, 1.0)		 
	# ****************** click on a tile ****************** 
	tile1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH ,   '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim )))) 
		)   
	tile1.click() 
	if (rand2):
		try:
			driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim))).click()
		except NoSuchElementException:          		
		    print('\n\r No Such Element Exception for finding 2nd tile')
   
	 
	#****************** click on submit buttion ****************** 
	driver.find_element_by_id("recaptcha-verify-button").click()

start = time()	 
url='...'
driver = webdriver.Firefox()
driver.get(url)

mainWin = driver.current_window_handle  

# move the driver to the first iFrame 
driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[0])

# *************  locate CheckBox  **************
CheckBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
        ) 

# *************  click CheckBox  ***************
wait_between(0.5, 0.7)  
# making click on captcha CheckBox 
CheckBox.click() 
 
#***************** back to main window **************************************
driver.switch_to_window(mainWin)  

wait_between(2.0, 2.5) 

# ************ switch to the second iframe by tag name ******************
driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[1])  
i=1
while i<130:
	print('\n\r{0}-th loop'.format(i))
	# ******** check if checkbox is checked at the 1st frame ***********
	driver.switch_to_window(mainWin)   
	WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe'))
        )  
	wait_between(1.0, 2.0)
	if check_exists_by_xpath('//span[@aria-checked="true"]'): 
                import winsound
		winsound.Beep(400,1500)
		write_stat(i, round(time()-start) - 1 ) # saving results into stat file
		break 
		
	driver.switch_to_window(mainWin)   
	# ********** To the second frame to solve pictures *************
	wait_between(0.3, 1.5) 
	driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[1]) 
	solve_images(driver)
	i=i+1




