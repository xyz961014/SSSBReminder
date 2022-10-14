from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import date, datetime, timedelta
import requests 
import time
import random
import argparse
import re
import os
import pymongo
from time import sleep
from tqdm import tqdm
import base64
import ipdb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true",
                        help="headless run browser")
    parser.add_argument("--distance", type=str, nargs="+",
                        help="get driving distance of two locations")
    parser.add_argument("--distance_mode", type=str, choices=["driving", "cycling", "transit"],
                        help="get driving distance of two locations")
    parser.add_argument("--max_retry", type=int, default=5,
                        help="retry when not crawled")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    return args


class GoogleMapWebSpider(object):
    def __init__(self, browser):
        self.url = "https://www.google.com/maps/dir/?hl=en"
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.apartment_urls = []

    def get_distance(self, place_from, place_to, mode="driving"):
        self.browser.get(self.url)
        #print("Successfully open url {}".format(self.url))
        # press accept cookies
        try:
            self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')))
            close_button = self.browser.find_element(by="xpath", value='//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
            close_button.click()
        except:
            print("No Cookie page")

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'tactile-searchbox-input')))
        input_boxes = self.browser.find_elements(by="class name", value="tactile-searchbox-input")
        box_from, box_to = input_boxes
        box_from.send_keys(place_from)
        box_to.send_keys(place_to)

        search_button = self.browser.find_element(by="xpath", value='//*[@id="directions-searchbox-1"]/button[1]')
        search_button.click()

        if mode == "driving":
            mode_button = self.browser.find_element(by="xpath", value='//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[2]/button')
        elif mode == "cycling":
            mode_button = self.browser.find_element(by="xpath", value='//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[5]/button')
        elif mode == "transit":
            mode_button = self.browser.find_element(by="xpath", value='//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[3]/button')
        mode_button.click()

        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]')))
        distance_blocks = self.browser.find_element(by="class name", value="XdKEzd").find_elements(by="tag name", value='div')
        time_block= distance_blocks[0]
        time_str = re.sub("\s", "", time_block.text)
        if "hr" in time_str and not "min" in time_str:
            parse_time = re.split("hr", time_str)
            hour = eval(parse_time[0])
            minute = 0
        elif not "hr" in time_str and "min" in time_str:
            parse_time = re.split("min", time_str)
            hour = 0
            minute = eval(parse_time[0])
        elif "hr" in time_str and "min" in time_str:
            parse_time = re.split("hr|min", time_str)
            hour = eval(parse_time[0])
            minute = eval(parse_time[1])

        if not mode == "transit":
            path_block = distance_blocks[1]
            path_str = re.sub("\s", "", path_block.text)
            if "km" in path_str:
                parse_path = re.split("km", re.sub(",", ".", path_str))
                km = eval(parse_path[0])
            elif "m" in path_str:
                parse_path = re.split("m", re.sub(",", ".", path_str))
                km = eval(parse_path[0]) / 1000
        else:
            km = None

        return {
                "from": place_from,
                "to": place_to,
                "mode": mode,
                "time": hour * 60 + minute,
                "distance": km
               }

    def quit(self):
        self.browser.quit()

def get_distance(place_from, place_to, mode):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    #print("{} From {} To {}.".format(mode, place_from, place_to))
    browser = webdriver.Chrome(options=options)
    spider = GoogleMapWebSpider(browser)
    distance = spider.get_distance(place_from, place_to, mode=mode)
    spider.quit()
    print("{} From {} To {} ({} min) Get.".format(mode, place_from, place_to, distance["time"]))

    return distance

def main(args):
    options = webdriver.ChromeOptions()
    options.headless = args.headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    #options.add_argument("--remote-debugging-port=9515")
    #options.add_argument("--proxy-server=127.0.0.1:8118")


    if args.distance:
        assert len(args.distance) == 2
        browser = webdriver.Chrome(options=options)
        spider = GoogleMapWebSpider(browser)
        distance = spider.get_distance(*args.distance, mode=args.distance_mode)
        print(distance)
        spider.quit()

if __name__ == "__main__":
    args = parse_args()
    main(args)
