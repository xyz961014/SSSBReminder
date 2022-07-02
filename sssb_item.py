import os
import re
import pymongo
import ipdb
import time
from datetime import date, datetime
import pytz

import socket
hostname = socket.gethostname()
mongo_path = "mongodb://localhost:27017"
if hostname == "xyz-ENVY-15":
    mongo_path = "mongodb://localhost:1027"
client = pymongo.MongoClient(mongo_path)
db = client["SSSB"]

class SSSBItem(object):
    def __init__(self):
        super().__init__()
        self._collection = None
        self._id = None
        self.update_time = None

    def get_info(self):
        info = {key: value for key, value in self.__dict__.items() if not re.match("_", key)}
        return info

    def save(self):
        self.update_time = get_now_time()
        obj = self.get_info()
        if self._id is None:
            self._collection.insert_one(obj)
        else:
            self._collection.update_one({"_id": self._id}, {"$set": obj})

    @classmethod
    def find_one(cls, json_object={}):
        one = cls._collection.find_one(json_object)
        if one is not None:
            item = cls(**one)
            item._id = one["_id"]
            item.update_time = one["update_time"]
        else:
            item = None
        return item

    @classmethod
    def find_many(cls, json_object={}):
        many = cls._collection.find(json_object)
        items = []
        for one in many:
            item = cls(**one)
            item._id = one["_id"]
            item.update_time = one["update_time"]
            items.append(item)
        return items


class ApartmentURL(SSSBItem):
    _collection = db["apartment_url"]
    def __init__(self, url,
                       electricity_include=False,
                       rent_free_june_and_july=False,
                       max_4_years=False,
                       **kwarg):
        super().__init__()
        self._collection = db["apartment_url"]
        self.url = url
        self.crawled = False

        self.electricity_include = electricity_include
        self.rent_free_june_and_july = rent_free_june_and_july
        self.max_4_years = max_4_years

    def save(self):
        if self._id is None:
            self.crawled_time = get_now_time()
            super().save()
        else:
            super().save()



class ApartmentInfo(SSSBItem):
    _collection = db["apartment_info"]
    def __init__(self, name, 
                      object_number, 
                      url,
                      housing_area=None,
                      address=None, 
                      accommodation_type=None,
                      living_space=None, 
                      monthly_rent=None, 
                      valid_from=None, 
                      end_date=None,
                      floor_drawing=None,
                      apartment_drawing=None,
                      application_ddl=None,
                      electricity_include=False,
                      rent_free_june_and_july=False,
                      max_4_years=False,
                      **kwarg):
        super().__init__()
        self._collection = db["apartment_info"]
        self.name = name
        self.object_number = object_number
        self.url = url
        self.housing_area = housing_area
        self.address = address
        self.accommodation_type = accommodation_type
        self.living_space = living_space
        self.monthly_rent = monthly_rent
        self.valid_from = valid_from
        self.end_date = end_date
        self.floor_drawing = floor_drawing
        self.apartment_drawing = apartment_drawing
        self.application_ddl = application_ddl
        self.electricity_include = electricity_include
        self.rent_free_june_and_july = rent_free_june_and_july
        self.max_4_years = max_4_years

    def is_active(self):
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        now_time = sweden_timezone.normalize(datetime.now().astimezone(tz=sweden_timezone))
        ddl = datetime.strptime(self.application_ddl, "%Y-%m-%d %H:%M:%S")
        ddl_time = datetime(ddl.year, ddl.month, ddl.day, 
                            ddl.hour, ddl.minute, ddl.second,
                            tzinfo=sweden_timezone)
        return ddl_time > now_time


class ApartmentStatus(SSSBItem):
    _collection = db["apartment_status"]
    def __init__(self, object_number, queue_len, most_credit, **kwargs):
        super().__init__()
        self._collection = db["apartment_status"]
        self.object_number = object_number
        self.queue_len = queue_len
        self.most_credit = most_credit


class ApartmentAmount(SSSBItem):
    _collection = db["apartment_amount"]
    def __init__(self, amount, **kwargs):
        super().__init__()
        self._collection = db["apartment_amount"]
        self.amount = amount


def get_now_time():
    time_obj = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)
    return time_str


