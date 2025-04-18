import os
import re
import pymongo
import ipdb
import time
from datetime import date, datetime, timedelta
import pytz
import json

from pymongo.errors import ServerSelectionTimeoutError

import socket
hostname = socket.gethostname()
mongo_path = "mongodb://mongo:27017"
mongo_path_local = "mongodb://localhost:1029"
try:
    client = pymongo.MongoClient(mongo_path, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
except ServerSelectionTimeoutError as e:
    client = pymongo.MongoClient(mongo_path_local, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
db = client["SSSB"]

from send_mail import send_mail, build_message
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from check_map import get_distance

import ipdb

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
            insert_res = self._collection.insert_one(obj)
            self._id = insert_res.inserted_id
        else:
            self._collection.update_one({"_id": self._id}, {"$set": obj})

    def get_update_time(self, timezone="Europe/Stockholm"):
        if timezone is None:
            return self.update_time
        timezone = pytz.timezone(timezone)
        update_time = datetime.strptime(self.update_time, "%Y-%m-%d %H:%M:%S")
        update_time = datetime(update_time.year, update_time.month, update_time.day, 
                               update_time.hour, update_time.minute, update_time.second,
                               tzinfo=pytz.timezone("UTC"))
        update_time = timezone.normalize(update_time.astimezone(tz=timezone))
        return update_time.strftime("%Y-%m-%d %H:%M:%S")

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
    def find_many(cls, json_object={}, sort=None, sort_order=1):
        many = cls._collection.find(json_object)
        if sort is not None:
            many = many.sort(sort, sort_order)
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
                       floor=None,
                       distances=None,
                       bid=None,
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
        self.floor = floor
        self.distances = distances
        self.bid = bid

    @classmethod
    def find_active_ones(cls):
        all_infos = cls.find_many()
        active_ones = [a for a in all_infos if a.is_active()]
        return active_ones

    def is_active(self):
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        now_time = sweden_timezone.normalize(datetime.now().astimezone(tz=sweden_timezone))
        application_ddl = self.application_ddl.replace("24:00:00", "23:59:59")
        ddl = datetime.strptime(application_ddl, "%Y-%m-%d %H:%M:%S")
        ddl_time = datetime(ddl.year, ddl.month, ddl.day, 
                            ddl.hour, ddl.minute, ddl.second,
                            tzinfo=sweden_timezone)
        return ddl_time > now_time

    def get_current_bid(self):
        bid = None
        statuses = ApartmentStatus.find_many({"object_number": self.object_number, "valid_from": self.valid_from},
                                             sort="update_time")
        if len(statuses) > 0:
            last_status = statuses[-1]
            bid = {
                    "queue_len": last_status.queue_len,
                    "most_credit": last_status.most_credit
                   }
            if self.is_active():
                self.bid = bid
                self.save()

        return bid

    def get_floor(self, floor=None):
        floor = self.floor if floor is None else floor
        if isinstance(floor, str):
            if floor.upper() == "SU":
                self.floor = -1
            elif floor.upper() == "GF":
                self.floor = 0
            else:
                try:
                    self.floor = int(floor)
                except ValueError:
                    self.floor = None
        elif isinstance(floor, int):
            self.floor = floor

        if self.floor is None:
            try:
                parse_address = self.address.split("/")
                apartment_num = parse_address[-1].strip()
                floor = int(apartment_num[1])
                floor += 10 * (int(apartment_num[0]) - 1)
                self.floor = floor
            except:
                self.floor = None
        return self.floor

    def get_distance(self, place_to, chromedriver_path, options=None):
        if not hasattr(self, "distances") or self.distances is None:
            self.distances = {
                "transit": [],
                "cycling": [],
            }
            try:
                transit_distance = get_distance(self.address, place_to, "transit", 
                                                chromedriver_path=chromedriver_path,
                                                options=options) 
                cycling_distance = get_distance(self.address, place_to, "cycling",
                                                chromedriver_path=chromedriver_path,
                                                options=options) 
                self.distances["transit"].append(transit_distance)
                self.distances["cycling"].append(cycling_distance)

            except Exception as e:
                print(e)
        else:
            transit_places = [d["to"] for d in self.distances["transit"]]
            cycling_places = [d["to"] for d in self.distances["cycling"]]
            if place_to not in transit_places:
                try:
                    transit_distance = get_distance(self.address, place_to, "transit",
                                                    chromedriver_path=chromedriver_path,
                                                    options=options) 
                    self.distances["transit"].append(transit_distance)
                except Exception as e:
                    print(e)
            if place_to not in cycling_places:
                try:
                    cycling_distance = get_distance(self.address, place_to, "cycling",
                                                    chromedriver_path=chromedriver_path,
                                                    options=options) 
                    self.distances["cycling"].append(cycling_distance)
                except Exception as e:
                    print(e)
        self.save()

        if place_to in self.distances.keys():
            return self.distances[place_to]
        else:
            return None

    def save(self):
        self.floor = self.get_floor()
        super().save()




class ApartmentStatus(SSSBItem):
    _collection = db["apartment_status"]
    def __init__(self, object_number, valid_from=None, queue_len=0, most_credit=0, **kwargs):
        super().__init__()
        self._collection = db["apartment_status"]
        self.object_number = object_number
        self.valid_from = valid_from
        self.queue_len = queue_len
        self.most_credit = most_credit


class ApartmentAmount(SSSBItem):
    _collection = db["apartment_amount"]
    def __init__(self, amount, **kwargs):
        super().__init__()
        self._collection = db["apartment_amount"]
        self.amount = amount


class PersonalFilter(SSSBItem):
    _collection = db["personal_filter"]
    def __init__(self, email, regions, types, living_space, rent,
                       address=None,
                       floor=None,
                       distance=0,
                       short_rent=False,
                       electricity_include=False,
                       rent_free_june_and_july=False,
                       max_4_years=False,
                       active=True,
                       current_credit=1e5,
                       credit_start=None,
                       recommendations=[],
                       **kwargs):
        super().__init__()
        self._collection = db["personal_filter"]
        self.email = email
        if credit_start is not None:
            self.credit_start = credit_start
        else:
            self.credit_start = self.get_credit_start(current_credit)
        self.current_credit = self.get_credit(save=False)
        self.regions = regions
        self.types = types
        self.address = address
        self.floor = floor
        self.living_space = living_space
        self.rent = rent
        if type(distance) == str:
            if not distance.strip() == "":
                self.distance = float(distance)
            else:
                self.distance = 0
        else:
            self.distance = distance
        self.short_rent = short_rent
        self.electricity_include = electricity_include
        self.rent_free_june_and_july = rent_free_june_and_july
        self.max_4_years = max_4_years
        self.active = active
        self.old_recommendations = recommendations
        self.recommendations = recommendations

    def get_credit(self, save=True):
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        now_time = sweden_timezone.normalize(datetime.now().astimezone(tz=sweden_timezone))
        start_date = datetime.strptime(self.credit_start, "%Y-%m-%d")
        start_date = datetime(start_date.year, start_date.month, start_date.day, 
                              tzinfo=sweden_timezone)
        self.current_credit = (now_time - start_date).days
        if save:
            self.save()
        return self.current_credit

    # def send_initial_mail(self):
    #     receivers = [self.email]
    #     link = "https://sssb.thufootball.tech/filter?id={}".format(self._id)

    #     curr_path = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(
    #                 os.path.join(curr_path, 'SSSB/SSSB/templates')))
    #     template = env.get_template('initial_mail.html')  
    #     msg = build_message(receivers, 
    #                         title="SSSB Filter built",
    #                         content=template.render(link=link))
    #     send_mail(receivers, msg)

    def unsubscribe(self):
        self.active = False
        self.save()

    def send_revised_mail(self):
        receivers = [self.email]
        link = "https://sssb.thufootball.tech/filter?id={}".format(self._id)

        curr_path = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(
                    os.path.join(curr_path, 'SSSB/SSSB/templates')))
        template = env.get_template('revising_mail.html')  
        msg = build_message(receivers, 
                            title="SSSB Filter revised",
                            content=template.render(link=link))
        send_mail(receivers, msg)

    def send_recommendations(self):
        receivers = [self.email]
        curr_recommendation_ids = self.recommendations
        last_recommendation_ids = self.old_recommendations
        new_ids = []
        unchange_ids = []
        for r_id in curr_recommendation_ids:
            if r_id in last_recommendation_ids:
                unchange_ids.append(r_id)
            else:
                new_ids.append(r_id)
        old_ids = []
        for r_id in last_recommendation_ids:
            if not r_id in curr_recommendation_ids:
                old_ids.append(r_id)
        new_recommendations = ApartmentInfo.find_many(
                {"object_number": {"$in": new_ids}}
                )
        unchange_recommendations = ApartmentInfo.find_many(
                {"object_number": {"$in": unchange_ids}}
                )
        old_recommendations = ApartmentInfo.find_many(
                {"object_number": {"$in": old_ids}}
                )

        def get_bid(recommendations):
            for r in recommendations:
                bid = r.get_current_bid()
                r.credit = bid["most_credit"]
                r.queue_len = bid["queue_len"]
                r.my_credit = self.get_credit()
            recommendations = sorted(recommendations, key=lambda x: x.credit)
            return recommendations

        def add_distance(candidates, distance_to):
            for i, c in enumerate(candidates):
                #candidates[i].get_distance(distance_to)
                if not hasattr(c, "distances") or c.distances is None:
                    continue
                candidates[i].distance_to = distance_to
                if distance_to in candidates[i].distances.keys():
                    candidates[i].distance = c.distances[distance_to]["cycling"]["distance"]
                    candidates[i].transit_time = c.distances[distance_to]["transit"]["time"]
                    candidates[i].cycling_time = c.distances[distance_to]["cycling"]["time"]
            return candidates

        #new_recommendations = add_distance(new_recommendations, "KTH")
        #unchange_recommendations = add_distance(unchange_recommendations, "KTH")
        #old_recommendations = add_distance(old_recommendations, "KTH")
        new_recommendations = get_bid(new_recommendations)
        unchange_recommendations = get_bid(unchange_recommendations)
        old_recommendations = get_bid(old_recommendations)

        curr_path = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(os.path.join(curr_path, 'SSSB/templates')))
        template = env.get_template('recommendation_mail.html')  

        link = "https://sssbreminder.xyzs.app/?filter_id={}".format(self._id)
        msg = build_message(receivers, 
                            title="New SSSB Reminder!",
                            content=template.render(new_recommendations=new_recommendations,
                                                    unchange_recommendations=unchange_recommendations,
                                                    old_recommendations=old_recommendations,
                                                    modify_url=link))
        send_mail(receivers, msg)


    @classmethod
    def get_credit_start(cls, credit):
        credit = int(credit)
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        now_time = sweden_timezone.normalize(datetime.now().astimezone(tz=sweden_timezone))
        start_time = now_time - timedelta(days=credit)
        return start_time.strftime("%Y-%m-%d")


def get_now_time():
    time_obj = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)
    return time_str

