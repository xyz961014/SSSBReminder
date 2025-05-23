from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime, timedelta
import requests 
import time
import random
import argparse
import re
import os
import sys
import pymongo
from time import sleep
from pprint import pprint
from tqdm import tqdm
from pathlib import Path
import base64
import emoji
import hashlib

from sssb_item import ApartmentURL, ApartmentInfo, ApartmentStatus, ApartmentAmount
from sssb_item import PersonalFilter

import ipdb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true",
                        help="headless run browser")
    parser.add_argument("--get_url", action="store_true",
                        help="get SSSB apartment urls")
    parser.add_argument("--check_url", action="store_true",
                        help="get SSSB apartment info and status")
    #parser.add_argument("--update_status", action="store_true",
    #                    help="update SSSB apartment status")
    parser.add_argument("--check_filter", action="store_true",
                        help="Check SSSB filters and send emails")
    parser.add_argument("--endless", action="store_true",
                        help="endless crawling")
    parser.add_argument("--crawl_interval", type=int, default=1800,
                        help="crawling interval seconds")
    parser.add_argument("--max_retry", type=int, default=5,
                        help="retry when not crawled")
    parser.add_argument("--credit_day_begin", type=str, default="2000-01-01",
                        help="set a date when credit days begin to accumulate")

    parser.add_argument("--local", action="store_true")

    args = parser.parse_args()
    return args


class SSSBWebSpider(object):
    def __init__(self, chromedriver_path, options):
        #self.apartments_url = "https://sssb.se/en/looking-for-housing/apply-for-apartment/available-apartments/?pagination=0&paginationantal=0"
        #self.new_apartments_url = "https://sssb.se/en/looking-for-housing/apply-for-apartment/new-constructions/?pagination=0&paginationantal=0"
        self.apartments_url = "https://minasidor.sssb.se/en/available-apartments/?pagination=0&paginationantal=0"
        self.chromedriver_path = chromedriver_path
        self.options = options
        service = ChromeService(executable_path=chromedriver_path)
        self.browser = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.apartment_urls = []

    def get_urls(self):
        amount = self.get_apartment_urls(self.apartments_url)
        apartment_amount = ApartmentAmount(amount=amount)
        apartment_amount.save()

    def get_apartment_urls(self, url):
        self.browser.get(url)
        print("Successfully open url {}".format(url))
        # close questionarie window
        #try:
        #    self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="WSA_LB2"]')))
        #    close_button = self.browser.find_element(by="xpath", value='//*[@id="WSA_LB2"]')
        #    close_button.click()
        #except:
        #    print("No questionarie window")
        self.wait.until(EC.visibility_of_element_located((By.ID, 'apartmentList')))
        available_apartments_area = self.browser.find_element(by="id", value="apartmentList")
        available_apartments = available_apartments_area.find_elements(by="class name", value="row")
        for apartment in tqdm(available_apartments, desc="Getting urls"):
            try:
                name_area = apartment.find_element(by="class name", value="apt-title")
                link = name_area.find_element(by="tag name", value="a")
                apartment_url = link.get_attribute("href")
                tags = apartment.find_elements(by="class name", value="rent-type")
                electricity_tag, free_june_july_tag, max_4_years_tag = False, False, False
                for tag in tags:
                    if tag.text == 'Electricity included':
                        electricity_tag = True
                    if tag.text == "10 mån hyra":
                        free_june_july_tag = True
                    if tag.text == "Max 4 years":
                        max_4_years_tag = True
                url_object = ApartmentURL(url=apartment_url, 
                                          crawled=False,
                                          electricity_include=electricity_tag,
                                          rent_free_june_and_july=free_june_july_tag,
                                          max_4_years=max_4_years_tag)
                url_object.save()
            except Exception as e:
                print("Getting URL with error: {}".format(e))

        return len(available_apartments)


    def check_apartment_urls(self):
        uncrawled_urls = ApartmentURL.find_many({"crawled": False})
        for url_item in tqdm(uncrawled_urls, file=sys.stdout, desc="Checking apartments"):

            time_delta = datetime.now() - datetime.strptime(url_item.update_time, "%Y-%m-%d %H:%M:%S")
            if time_delta > timedelta(hours=6):
                url_item.crawled = True
                url_item.save()
                tqdm.write(f"URL {url_item.url} expired.")
                continue

            try:
                self.check_apartment_url(url_item)
                #tqdm.write("complete")
            except Exception as e:
                print("Error: {}, Skipped".format(e))



    def check_apartment_url(self, url_item):
        url = url_item.url
        (name, 
         object_number, 
         housing_area, 
         address, 
         accommodation_type, 
         living_space, 
         floor,
         monthly_rent, 
         valid_from, 
         end_date, 
         floor_drawing,
         apartment_drawing,
         ddl,
         queue_len,
         most_credit) = self.get_url_info(url)

        status_item = ApartmentStatus(object_number=object_number, 
                                      valid_from=valid_from,
                                      queue_len=queue_len, 
                                      most_credit=most_credit)
        status_item.save()

        if ApartmentInfo.find_one({"object_number": object_number, "valid_from": valid_from}) is None:
            # add new apartment
            info_item = ApartmentInfo(name=name,
                                      object_number=object_number,
                                      url=url,
                                      housing_area=housing_area,
                                      address=address,
                                      accommodation_type=accommodation_type,
                                      living_space=living_space,
                                      floor=floor,
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
            #info_item.get_distance("KTH", chromedriver_path=self.chromedriver_path, options=self.options)
        else:
            # update apartment info
            info_item = ApartmentInfo.find_one({"object_number": object_number, "valid_from": valid_from})
            info_item.url = url
            info_item.monthly_rent = monthly_rent
            info_item.end_date = end_date
            info_item.application_ddl = ddl
            info_item.electricity_include = url_item.electricity_include
            info_item.rent_free_june_and_july = url_item.rent_free_june_and_july
            info_item.max_4_years = url_item.max_4_years
            #if not hasattr(info_item, "distances") or info_item.distances is None or info_item.distances == {}:
            #    info_item.get_distance("KTH", chromedriver_path=self.chromedriver_path, options=self.options)

        url_item.crawled = True
        url_item.save()

        info_item.get_floor(floor)
        info_item.get_current_bid()
        info_item.save()

    def get_url_info(self, url):
        #self.browser.execute_script("window.open();")
        #self.browser.switch_to.window(self.browser.window_handles[-1]) 
        self.browser.get(url)
        
        self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
        title = self.browser.find_element(by="tag name", value="h1")
        name = title.text
        address = name
        object_number = hashlib.sha256(name.encode()).hexdigest()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'apt-address')))
        subtitle = self.browser.find_element(by="class name", value="apt-address")
        accommodation_type = subtitle.text


        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'property-details')))
        attributes_area = self.browser.find_element(by="class name", value="property-details")
        attribute_key_columns = attributes_area.find_elements(by="class name", value="apt-details-headers")
        attribute_value_columns = attributes_area.find_elements(by="class name", value="apt-details-data")
        attribute_keys = []
        for key_column in attribute_key_columns:
            attribute_keys.extend(key_column.find_elements(by="tag name", value="li"))
        attribute_values = []
        for value_column in attribute_value_columns:
            attribute_values.extend(value_column.find_elements(by="tag name", value="li"))

        attributes = {key.text: value.text for key, value in list(zip(attribute_keys, attribute_values))}

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'pdf-links')))
        drawing_area = self.browser.find_element(by="class name", value="ObjektDokument")
        buttons = drawing_area.find_elements(by="class name", value="btn")
        apartment_drawing, floor_drawing = None, None
        try:
            for button in buttons:
                button_name = button.text.upper()
                button_url = button.get_attribute("href")
                resource_name = "./resources/{}_{}.pdf".format(object_number, button_name) 
                if not os.path.exists(resource_name):
                    r = requests.get(button_url, verify=False) 
                    if button_name.upper() == "APARTMENT DRAWING":
                        apartment_drawing = resource_name 
                    elif button_name.upper() == "FLOOR DRAWING":
                        floor_drawing = resource_name 
                    with open(resource_name, "wb") as code:
                         code.write(r.content)
        except Exception as e:
            pass

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

        housing_area = attributes["Area:"] if "Area:" in attributes.keys() else None

        living_space = attributes["Living space:"] \
                       if "Living space:" in attributes.keys() else None
        if living_space is not None:
            living_space = re.sub("[^0-9]", "", living_space)
            living_space = int(living_space)

        floor = attributes["Floor:"] if "Floor:" in attributes.keys() else None

        monthly_rent = attributes["Rent:"] if "Rent:" in attributes.keys() else None
        if monthly_rent is not None:
            monthly_rent = re.sub("[^0-9]", "", monthly_rent)
            monthly_rent = int(monthly_rent)

        valid_from = attributes["Moving in:"] if "Moving in:" in attributes.keys() else None
        end_date = attributes["The rental agreement ends:"] \
                   if "The rental agreement ends:" in attributes.keys() else None

        #self.browser.close()
        #self.browser.switch_to.window(self.browser.window_handles[-1]) 

        return (name, 
                object_number, 
                housing_area, 
                address, 
                accommodation_type, 
                living_space, 
                floor,
                monthly_rent, 
                valid_from, 
                end_date, 
                floor_drawing,
                apartment_drawing,
                ddl,
                queue_len,
                most_credit)


    def quit(self):
        self.browser.quit()


def check_personal_filters():
    filters = PersonalFilter.find_many({"active": True})
    for f in tqdm(filters, desc="Checking filters"):
        info_condition = {}
        if f.regions is not None and len(f.regions) > 0:
            info_condition["housing_area"] = {"$in": f.regions}
        if f.types is not None and len(f.types) > 0:
            info_condition["accommodation_type"] = {"$in": f.types}
        if f.address is not None and type(f.address) is str and f.address.strip() != "":
            info_condition["address"] = {"$regex": f.address, "$options": "i"}

        if f.living_space is not None:
            if f.living_space["min"]:
                if not "living_space" in info_condition.keys():
                    info_condition["living_space"] = {}
                info_condition["living_space"]["$gte"] = int(f.living_space["min"])
            if f.living_space["max"]:
                if not "living_space" in info_condition.keys():
                    info_condition["living_space"] = {}
                info_condition["living_space"]["$lte"] = int(f.living_space["max"])
        if f.rent is not None:
            if f.rent["min"]:
                if not "monthly_rent" in info_condition.keys():
                    info_condition["monthly_rent"] = {}
                info_condition["monthly_rent"]["$gte"] = int(f.rent["min"])
            if f.rent["max"]:
                if not "monthly_rent" in info_condition.keys():
                    info_condition["monthly_rent"] = {}
                info_condition["monthly_rent"]["$lte"] = int(f.rent["max"])
        if f.floor is not None:
            if f.floor["min"]:
                if not "floor" in info_condition.keys():
                    info_condition["floor"] = {}
                info_condition["floor"]["$gte"] = int(f.floor["min"])
            if f.floor["max"]:
                if not "floor" in info_condition.keys():
                    info_condition["floor"] = {}
                info_condition["floor"]["$lte"] = int(f.floor["max"])

        if f.electricity_include is not None:
            info_condition["electricity_include"] = f.electricity_include
        if f.rent_free_june_and_july is not None:
            info_condition["rent_free_june_and_july"] = f.rent_free_june_and_july
        if f.max_4_years is not None:
            info_condition["max_4_years"] = f.max_4_years
        if f.short_rent is not None:
            if f.short_rent:
                info_condition["end_date"] = {"$ne": None}
            else:
                info_condition["end_date"] = None
        candidates = ApartmentInfo.find_many(info_condition)
        candidates = [c for c in candidates if c.is_active()]
        person_credit = f.get_credit()
        possible_cands = [c for c in candidates 
                          if person_credit >= c.get_current_bid()["most_credit"]]
        if len(possible_cands) > 0:
            # THERE ARE CHANCES!
            possible_object_numbers = [c.object_number for c in possible_cands]
            #if True:
            if not f.recommendations == possible_object_numbers:
                # New recommendations!
                # save recommendations
                f.old_recommendations = f.recommendations
                f.recommendations = possible_object_numbers
                f.save()

                # Send mail
                f.send_recommendations()
            else:
                print("Duplicate recommendations. Skipped.")


def main(args):
    current_dir = Path(__file__).parent
    if args.local:
        chrome_path = (current_dir / 'chrome-linux64/chrome').as_posix()
        #chrome_path = (current_dir / 'chrome-headless-shell-linux64/chrome-headless-shell').as_posix()
        chromedriver_path = (current_dir / 'chromedriver-linux64/chromedriver').as_posix()
        service = ChromeService(executable_path=chromedriver_path)

        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        chrome_options.headless = args.headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

    else:
        chrome_path = '/chrome-headless-shell-linux64/chrome-headless-shell'
        chromedriver_path = '/chromedriver-linux64/chromedriver'
        service = ChromeService(executable_path=chromedriver_path)

        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        chrome_options.headless = args.headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--single-process")

    func = ""
    if args.endless:
        while True:
            start_time = time.time()
            success = False
            for _ in range(args.max_retry):
                try:
                    if not success:
                        if args.get_url:
                            func = "get_url"
                            tqdm.write(func)
                            spider = SSSBWebSpider(chromedriver_path, chrome_options)
                            spider.get_urls()
                        if args.check_url:
                            func = "check_url"
                            tqdm.write(func)
                            spider = SSSBWebSpider(chromedriver_path, chrome_options)
                            spider.check_apartment_urls()
                        if args.check_filter:
                            func = "check_filter"
                            tqdm.write(func)
                            check_personal_filters()

                        success = True
                except Exception as e:
                    print(f"{func} Error occurs: {e}")
                finally:
                    if args.get_url or args.check_url:
                        spider.quit()
            end_time = time.time()
            time_used = end_time - start_time
            if time_used < args.crawl_interval:
                restart_time = (datetime.now() + \
                                timedelta(seconds=args.crawl_interval - time_used)).strftime("%Y-%m-%d %H:%M:%S")
                print("{} Sleep {:5.3f}s, Restart at {}".format(func, args.crawl_interval - time_used, restart_time))
                time.sleep(args.crawl_interval - time_used)
            else:
                print("{} No sleep, Restart at {}".format(func, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        if args.get_url:
            spider = SSSBWebSpider(chromedriver_path, chrome_options)
            spider.get_urls()
            spider.quit()
        if args.check_url:
            spider = SSSBWebSpider(chromedriver_path, chrome_options)
            spider.check_apartment_urls()
            spider.quit()
        if args.check_filter:
            check_personal_filters()

if __name__ == "__main__":
    args = parse_args()
    main(args)
