from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import date, datetime, timedelta
from sssb_item import ApartmentURL, ApartmentInfo, ApartmentStatus
import requests 
import time
import random
import argparse
import re
import os
import pymongo
from time import sleep
from pprint import pprint
from tqdm import tqdm
import base64
import emoji
import ipdb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true",
                        help="headless run browser")
    parser.add_argument("--get_url", action="store_true",
                        help="get SSSB apartment urls")
    parser.add_argument("--check_url", action="store_true",
                        help="get SSSB apartment info and status")
    parser.add_argument("--update_status", action="store_true",
                        help="update SSSB apartment status")
    parser.add_argument("--endless", action="store_true",
                        help="endless crawling")
    parser.add_argument("--crawl_interval", type=int, default=3600,
                        help="crawling interval seconds")
    parser.add_argument("--credit_day_begin", type=str, default="2000-01-01",
                        help="set a date when credit days begin to accumulate")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    return args


class SSSBWebSpider(object):
    def __init__(self, browser):
        self.apartments_url = "https://sssb.se/en/looking-for-housing/apply-for-apartment/available-apartments/?pagination=0&paginationantal=0"
        self.new_apartments_url = "https://sssb.se/en/looking-for-housing/apply-for-apartment/new-constructions//?pagination=0&paginationantal=0"
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.apartment_urls = []

    def get_urls(self):
        self.get_apartment_urls(self.apartments_url)
        self.get_apartment_urls(self.new_apartments_url)

    def get_apartment_urls(self, url):
        self.browser.get(url)
        print("Successfully open url {}".format(url))
        # close questionarie window
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="WSA_LB2"]')))
            close_button = self.browser.find_element(by="xpath", value='//*[@id="WSA_LB2"]')
            close_button.click()
        except:
            print("No questionarie window")
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Objektlistabilder')))
        available_apartments_area = self.browser.find_element(by="class name", value="Objektlistabilder")
        available_apartments = available_apartments_area.find_elements(by="class name", value="ObjektListItem")
        for apartment in tqdm(available_apartments, desc="Getting urls"):
            name_area = apartment.find_element(by="class name", value="ObjektTyp")
            link = name_area.find_element(by="tag name", value="a")
            apartment_url = link.get_attribute("href")
            if ApartmentURL.find_one({"url": apartment_url, "crawled": False}) is None:
                electricity_tag = len(apartment.find_elements(by="class name", value="Egenskap-1036")) > 0
                free_june_july_tag = len(apartment.find_elements(by="class name", value="Egenskap-3025")) > 0
                max_4_years_tag = len(apartment.find_elements(by="class name", value="Egenskap-1093")) > 0
                url_object = ApartmentURL(url=apartment_url, 
                                          crawled=False,
                                          electricity_inlcude=electricity_tag,
                                          rent_free_june_and_july=free_june_july_tag,
                                          max_4_years=max_4_years_tag)
                url_object.save()

    def check_apartment_urls(self):
        uncrawled_urls = ApartmentURL.find_many({"crawled": False})
        for url_item in tqdm(uncrawled_urls, desc="Checking apartments"):
            self.check_apartment(url_item)

    def check_apartment(self, url_item):
        url = url_item.url
        self.browser.execute_script("window.open();")
        self.browser.switch_to.window(self.browser.window_handles[-1]) 
        self.browser.get(url)
        
        self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
        title = self.browser.find_element(by="tag name", value="h1")
        name = title.text

        self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'em')))
        subtitle_content = self.browser.find_element(by="tag name", value="em")
        object_number = subtitle_content.text

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ObjektDetaljer')))
        attributes_area = self.browser.find_element(by="class name", value="ObjektDetaljer")
        attribute_keys = attributes_area.find_elements(by="tag name", value="dt")
        attribute_values = attributes_area.find_elements(by="tag name", value="dd")
        attributes = {key.text: value.text for key, value in list(zip(attribute_keys, attribute_values))}

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ObjektDokument')))
        drawing_area = self.browser.find_element(by="class name", value="ObjektDokument")
        buttons = drawing_area.find_elements(by="class name", value="btn")
        apartment_drawing, floor_drawing = None, None
        for button in buttons:
            button_name = button.text
            button_url = button.get_attribute("href")
            resource_name = "./resources/{}_{}.pdf".format(object_number, button_name) 
            if not os.path.exists(resource_name):
                r = requests.get(button_url) 
                if button_name == "APARTMENT DRAWING":
                    apartment_drawing = resource_name 
                elif button_name == "FLOOR DRAWING":
                    floor_drawing = resource_name 
                with open(resource_name, "wb") as code:
                     code.write(r.content)

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Objektintressestatus')))
        apartment_status = self.browser.find_element(by='class name', value='Objektintressestatus')
        queue_len_sentences = apartment_status.text.split(".")
        if queue_len_sentences[0].strip() == "This object has not yet received any applications":
            queue_len = 0
            most_credit = 0
        else:
            queue_len_sentence, most_credit_sentence, _ = apartment_status.text.split(".")
            queue_len = int(queue_len_sentence.split()[-2])
            most_credit = int(most_credit_sentence.split()[-3])

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'IntresseMeddelande')))
        ddl_area = self.browser.find_element(by='class name', value='IntresseMeddelande')
        ddl_sentence = ddl_area.text.split(".")[0]
        ddl_date, ddl_time = ddl_sentence.split()[-3], ddl_sentence.split()[-1]
        ddl = "{} {}:00".format(ddl_date, ddl_time)

        housing_area = attributes["Housing area:"] if "Housing area:" in attributes.keys() else None
        address = attributes["Address:"] if "Address:" in attributes.keys() else None
        accommodation_type = attributes["Type of accommodation:"]  \
                             if "Type of accommodation:" in attributes.keys() else None

        living_space = attributes["Living space (approx.):"] \
                       if "Living space (approx.):" in attributes.keys() else None
        if living_space is not None:
            living_space = re.sub("[^0-9]", "", living_space)
            living_space = int(living_space)

        monthly_rent = attributes["Monthly rent:"] if "Monthly rent:" in attributes.keys() else None
        if monthly_rent is not None:
            monthly_rent = re.sub("[^0-9]", "", monthly_rent)
            monthly_rent = int(monthly_rent)

        valid_from = attributes["The rental agreement is valid from:"] \
                     if "The rental agreement is valid from:" in attributes.keys() else None
        end_date = attributes["The rental agreement ends:"] \
                   if "The rental agreement ends:" in attributes.keys() else None

        if ApartmentInfo.find_one({"object_number": object_number}) is None:
            # add new apartment
            info_item = ApartmentInfo(name=name,
                                      object_number=object_number,
                                      housing_area=housing_area,
                                      address=address,
                                      accommodation_type=accommodation_type,
                                      living_space=living_space,
                                      monthly_rent=monthly_rent,
                                      valid_from=valid_from,
                                      end_date=end_date,
                                      floor_drawing=floor_drawing,
                                      apartment_drawing=apartment_drawing,
                                      application_ddl=ddl,
                                      electricity_include=url_item.electricity_include,
                                      rent_free_june_and_july=url_item.rent_free_june_and_july,
                                      max_4_years=url_item.max_4_years
                                      )
            info_item.save()
        #else:
        #    # update apartment info
        #    info_item = ApartmentInfo.find_one({"object_number": object_number})

        status_item = ApartmentStatus(object_number=object_number, queue_len=queue_len, most_credit=most_credit)
        status_item.save()

        url_item.crawled = True
        url_item.save()

        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1]) 

    def quit(self):
        self.browser.quit()



def main(args):
    options = webdriver.ChromeOptions()
    options.headless = args.headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9515")
    options.add_argument("--proxy-server=127.0.0.1:8118")

    date_begin = datetime.strptime(args.credit_day_begin, "%Y-%m-%d")

    if args.get_url:
        if args.endless:
            while True:
                start_time = time.time()
                try:
                    browser = webdriver.Chrome(options=options)
                    spider = SSSBWebSpider(browser)
                    spider.get_urls()
                    spider.quit()
                except Exception as e:
                    print("Error occurs: ", e)
                end_time = time.time()
                time_used = end_time - start_time
                if time_used < args.crawl_interval:
                    restart_time = (datetime.now() + \
                                    timedelta(seconds=args.crawl_interval - time_used)).strftime("%Y-%m-%d %H:%M:%S")
                    print("Sleep {:5.3f}s, Restart at {}".format(args.crawl_interval - time_used, restart_time))
                    time.sleep(args.crawl_interval - time_used)
                else:
                    print("No sleep, Restart at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            browser = webdriver.Chrome(options=options)
            spider = SSSBWebSpider(browser)
            spider.get_urls()
            spider.quit()

    elif args.check_url:
        if args.endless:
            while True:
                start_time = time.time()
                try:
                    browser = webdriver.Chrome(options=options)
                    spider = SSSBWebSpider(browser)
                    spider.check_apartment_urls()
                    spider.quit()
                except Exception as e:
                    print("Error occurs: ", e)
                end_time = time.time()
                time_used = end_time - start_time
                if time_used < args.crawl_interval:
                    restart_time = (datetime.now() + \
                                    timedelta(seconds=args.crawl_interval - time_used)).strftime("%Y-%m-%d %H:%M:%S")
                    print("Sleep {:5.3f}s, Restart at {}".format(args.crawl_interval - time_used, restart_time))
                    time.sleep(args.crawl_interval - time_used)
                else:
                    print("No sleep, Restart at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            browser = webdriver.Chrome(options=options)
            spider = SSSBWebSpider(browser)
            spider.check_apartment_urls()
            spider.quit()
    else:
        print("Please select a function")


if __name__ == "__main__":
    args = parse_args()
    main(args)
