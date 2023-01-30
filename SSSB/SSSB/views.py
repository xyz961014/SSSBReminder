# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pprint import pprint

from datetime import date, datetime
import math
import json
import time
import pymongo
from bson import ObjectId
from pprint import pprint

import os
import sys
curr_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(curr_path, "../.."))
from sssb_item import ApartmentInfo, ApartmentURL, ApartmentStatus, ApartmentAmount
from sssb_item import PersonalFilter

import socket
hostname = socket.gethostname()

template_path = "/root/projects/SSSBReminder/SSSB/SSSB/templates"
if hostname == "xyz-ENVY-15":
    template_path = "/home/xyz/Documents/Projects/web_check/SSSBReminder/SSSB/SSSB/templates"

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader(template_path))


#mongo_path = "mongodb://localhost:27017"
#if hostname == "xyz-ENVY-15":
#    mongo_path = "mongodb://localhost:1027"
#client = pymongo.MongoClient(mongo_path)
#db = client["SSSB"]
#url_collection = db["apartment_url"]
#info_collection = db["apartment_info"]
#status_collection = db["apartment_status"]

def new_filter(request):
    email = request.POST.get("email", None)
    if email is not None:
        credit = request.POST.get("credit", 0)
        regions = request.POST.getlist("region", [])
        types = request.POST.getlist("type", [])
        distance = request.POST.get("distance", 0)
        floor_min = request.POST.get("floor_min", None)
        floor_max = request.POST.get("floor_max", None)
        floor_unspecified = request.POST.get("floor_unspecified", None) == "on"
        space_min = request.POST.get("space_min", None)
        space_max = request.POST.get("space_max", None)
        space_unspecified = request.POST.get("space_unspecified", None) == "on"
        rent_min = request.POST.get("rent_min", None)
        rent_max = request.POST.get("rent_max", None)
        rent_unspecified = request.POST.get("rent_unspecified", None) == "on"
        short_rent = request.POST.get("short_rent", None) == "on"
        electricity_include = request.POST.get("electricity_include", None) == "on"
        rent_free_june_and_july = request.POST.get("rent_free_june_and_july", None) == "on"
        max_4_years = request.POST.get("max_4_years", None) == "on"

        floor = {
                "unspecified": floor_unspecified,
                "min": floor_min,
                "max": floor_max
                            }
        space = {
                "unspecified": space_unspecified,
                "min": space_min,
                "max": space_max
                            }
        rent = {
                "unspecified": rent_unspecified,
                "min": rent_min,
                "max": rent_max
                            }
        personal_filter = PersonalFilter(
                              email=email,
                              current_credit=credit,
                              regions=regions,
                              types=types,
                              floor=floor,
                              space=space,
                              rent=rent,
                              distance=distance,
                              short_rent=short_rent,
                              electricity_include=electricity_include,
                              rent_free_june_and_july=rent_free_june_and_july,
                              max_4_years=max_4_years)

        personal_filter.save()
        personal_filter.send_initial_mail()


    html_data = {
            "region_list": get_regions(),
            "type_list": get_types(),
            "space_boundaries": get_space_boundaries(),
            "rent_boundaries": get_rent_boundaries(),
            }
    return render(request, "new_filter.html", html_data)


def index(request):
    html_data = {}
    return render(request, "index.html", html_data)

def search_apartments(request):

    html_data = {
            "region_list": get_regions(),
            "type_list": get_types(),
            "space_boundaries": get_space_boundaries(),
            "rent_boundaries": get_rent_boundaries(),
            }

    MAX = 1e8
    floor_boundaries = get_floor_boundaries()
    space_boundaries = get_space_boundaries()
    space_boundaries = get_space_boundaries()
    rent_boundaries = get_rent_boundaries()

    show_expired = request.POST.get("show_expired", "off") == "on"
    credit = request.POST.get("credit", 0)
    regions = request.POST.getlist("region", [r.name for r in html_data["region_list"]])
    types = request.POST.getlist("type", [t.name for t in html_data["type_list"]])
    distance_to = request.POST.get("distance_to", "KTH")
    distance = request.POST.get("distance", 0)
    bike_time = request.POST.get("bike_time", 0)
    bus_time = request.POST.get("bus_time", 0)
    floor_min = request.POST.get("floor_min", floor_boundaries.min)
    floor_max = request.POST.get("floor_max", floor_boundaries.max)
    floor_unspecified = request.POST.get("floor_unspecified", None) == "on"
    space_min = request.POST.get("space_min", space_boundaries.min)
    space_max = request.POST.get("space_max", space_boundaries.max)
    space_unspecified = request.POST.get("space_unspecified", None) == "on"
    rent_min = request.POST.get("rent_min", rent_boundaries.min)
    rent_max = request.POST.get("rent_max", rent_boundaries.max)
    rent_unspecified = request.POST.get("rent_unspecified", None) == "on"
    short_rent = request.POST.get("short_rent", None) == "on"
    electricity_include = request.POST.get("electricity_include", None) == "on"
    rent_free_june_and_july = request.POST.get("rent_free_june_and_july", None) == "on"
    max_4_years = request.POST.get("max_4_years", "off") == "on"

    sort_key = request.GET.get("sort_key", None)
    sort_order = request.GET.get("sort_order", "asc")


    for i, region in enumerate(html_data["region_list"]):
        if region.name in regions:
            html_data["region_list"][i].selected = True
        else:
            html_data["region_list"][i].selected = False

    for i, typ in enumerate(html_data["type_list"]):
        if typ.name in types:
            html_data["type_list"][i].selected = True
        else:
            html_data["type_list"][i].selected = False


    html_data.update({
            "show_expired": show_expired,
            "credit": credit,
            "distance": distance,
            "bike_time": bike_time,
            "bus_time": bus_time,
            "floor_min": floor_min,
            "floor_max": floor_max,
            "space_min": space_min,
            "space_max": space_max,
            "rent_min": rent_min,
            "rent_max": rent_max,
            "floor_unspecified": floor_unspecified,
            "space_unspecified": space_unspecified,
            "rent_unspecified": rent_unspecified,
            "short_rent": short_rent,
            "electricity_include": electricity_include,
            "rent_free_june_and_july": rent_free_june_and_july,
            "max_4_years": max_4_years,
            "sort_key": sort_key,
            "sort_order": sort_order
        })

    def get_apartments():
        info_condition = {
                "housing_area": {"$in": regions},
                "accommodation_type": {"$in": types},
                         }
        if not space_unspecified:
            if space_min:
                if not "living_space" in info_condition.keys():
                    info_condition["living_space"] = {}
                info_condition["living_space"]["$gte"] = int(space_min)
            if space_max:
                if not "living_space" in info_condition.keys():
                    info_condition["living_space"] = {}
                info_condition["living_space"]["$lte"] = int(space_max)
        if not rent_unspecified:
            if rent_min:
                if not "monthly_rent" in info_condition.keys():
                    info_condition["monthly_rent"] = {}
                info_condition["monthly_rent"]["$gte"] = int(rent_min)
            if rent_max:
                if not "monthly_rent" in info_condition.keys():
                    info_condition["monthly_rent"] = {}
                info_condition["monthly_rent"]["$lte"] = int(rent_max)
        if short_rent:
            info_condition["end_date"] = {"$ne": None}
        if electricity_include:
            info_condition["electricity_include"] = electricity_include
        if rent_free_june_and_july:
            info_condition["rent_free_june_and_july"] = rent_free_june_and_july
        if max_4_years:
            info_condition["max_4_years"] = max_4_years

        candidates = ApartmentInfo.find_many(info_condition)

        for i, c in enumerate(candidates):
            candidates[i].credit = c.get_current_bid()["most_credit"]
            candidates[i].floor = c.get_floor()

        if not show_expired:
            candidates = [c for c in candidates if c.is_active()]

        if int(credit) > 0:
            candidates = [c for c in candidates if int(credit) >= c.credit]

        if not floor_unspecified:
            if floor_min:
                candidates = [c for c in candidates if c.floor is None or int(floor_min) <= c.floor]
            if floor_max:
                candidates = [c for c in candidates if c.floor is None or int(floor_max) >= c.floor]

        if distance_to:
            for i, c in enumerate(candidates):
                print("HAHAHA", i)
                #candidates[i].get_distance(distance_to)
                if not hasattr(c, "distances") or c.distances is None:
                    continue
                candidates[i].distance_to = distance_to
                if distance_to in candidates[i].distances.keys():
                    candidates[i].distance = c.distances[distance_to]["cycling"]["distance"]
                    candidates[i].transit_time = c.distances[distance_to]["transit"]["time"]
                    candidates[i].cycling_time = c.distances[distance_to]["cycling"]["time"]

            if float(distance) > 0:
                candidates = [c for c in candidates 
                              if distance_to not in c.distances.keys() or 
                                 c.distances[distance_to]["cycling"]["distance"] <= float(distance)]
            if float(bus_time) > 0:
                candidates = [c for c in candidates 
                              if distance_to not in c.distances.keys() or 
                                 c.distances[distance_to]["transit"]["time"] <= float(bus_time)]
            if float(bike_time) > 0:
                candidates = [c for c in candidates 
                              if distance_to not in c.distances.keys() or 
                                 c.distances[distance_to]["cycling"]["time"] <= float(bike_time)]

        return candidates

    apartments = get_apartments()
    if sort_key is not None:
        if sort_key == "region":
            apartments = sorted(apartments, key=lambda x: x.distances[x.distance_to]["cycling"]["distance"], 
                                            reverse=sort_order=="desc")
        else:
            apartments = sorted(apartments, key=lambda x: getattr(x, sort_key), reverse=sort_order=="desc")
    html_data["apartments"] = apartments

    return render(request, "search_apartments.html", html_data)


def filter_info(request):
    f_id = request.GET.get("id")
    personal_filter = PersonalFilter.find_one({"_id": ObjectId(f_id)})
    personal_filter.get_credit()
    if not personal_filter.active:
        return HttpResponse("Not an active subscription.")
    filter_dict = {key: dict2obj(value) 
                   for key, value in personal_filter.get_info().items()}
    filter_dict["id"] = f_id
    filter_dict["region_list"] = get_regions()
    filter_dict["type_list"] = get_types()

    email = request.POST.get("email", None)
    if email is not None:
        # edit subscription
        credit = request.POST.get("credit", 0)
        personal_filter.distance = request.POST.get("distance", 0)
        personal_filter.credit_start = PersonalFilter.get_credit_start(credit)
        personal_filter.regions = request.POST.getlist("region", [])
        personal_filter.types = request.POST.getlist("type", [])
        floor_min = request.POST.get("floor_min", None)
        floor_max = request.POST.get("floor_max", None)
        floor_unspecified = request.POST.get("floor_unspecified", None) == "on"
        space_min = request.POST.get("space_min", None)
        space_max = request.POST.get("space_max", None)
        space_unspecified = request.POST.get("space_unspecified", None) == "on"
        rent_min = request.POST.get("rent_min", None)
        rent_max = request.POST.get("rent_max", None)
        rent_unspecified = request.POST.get("rent_unspecified", None) == "on"
        personal_filter.short_rent = request.POST.get("short_rent", None) == "on"
        personal_filter.electricity_include = request.POST.get("electricity_include", None) == "on"
        personal_filter.rent_free_june_and_july = request.POST.get("rent_free_june_and_july", None) == "on"
        floor = {
                "unspecified": floor_unspecified,
                "min": int(floor_min) if floor_min is not None else None,
                "max": int(floor_max) if floor_max is not None else None
                            }
        space = {
                "unspecified": space_unspecified,
                "min": int(space_min) if space_min is not None else None,
                "max": int(space_max) if space_max is not None else None
                            }
        rent = {
                "unspecified": rent_unspecified,
                "min": int(rent_min) if rent_min is not None else None,
                "max": int(rent_max) if rent_max is not None else None
                            }
        personal_filter.floor = floor
        personal_filter.space = space
        personal_filter.rent = rent

        personal_filter.save()
        personal_filter.send_revised_mail()

    return render(request, "filter.html", filter_dict)


def unsubscribe_filter(request):
    f_id = request.GET.get("id")
    personal_filter = PersonalFilter.find_one({"_id": ObjectId(f_id)})
    personal_filter.unsubscribe()
    return HttpResponse("Unsubscribed!")


def available_apartments(request):
    #page = Page(layout=Page.SimplePageLayout)
    amount_line = get_amount_line()
    #page.add(
    #    amount_line,
    #        )
    turn_back = """<a href="/">Back</a>"""
    return HttpResponse(turn_back + amount_line.render_embed())


def apartment_status(request):

    input_area = """
   <head>
      <title>Apartment Info</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
   </head>
       <div style="padding: 100px 100px 10px;">
           <form method="get">
               <div class="row">
                   <div class="col-lg-6">
                       <div class="input-group">
                           <span class="input-group-addon">Object number</span> 
                           <input name="object_number" type="text" class="form-control">
                           <span class="input-group-btn">
                               <button class="btn btn-default" type="submit">
                               Go!
                               </button>
                           </span>
                       </div>
                   </div>
               </div>
           </form>
       </div>
                 """

    object_number = request.GET.get("object_number", None)
    if object_number is not None:
        object_info_table = get_apartment_info_table(object_number) 
        object_line = get_apartment_line(object_number)
        return HttpResponse(input_area + \
                            object_info_table + \
                            "<div class='col-lg-12'>" + \
                            object_line.render_embed() + \
                            "</div>")
    else:
        return HttpResponse(input_area)


# Charts

def get_amount_line():
    amounts = ApartmentAmount.find_many()
    times = []
    counts = []
    for amount in amounts:
        times.append(amount.get_update_time())
        counts.append(amount.amount)
    c = (
        Line(init_opts=opts.InitOpts())
        .add_xaxis(xaxis_data=times)
        .add_yaxis(
            series_name="Number of available apartments",
            y_axis=counts,
            is_symbol_show=False,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Available apartments", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


def get_apartment_info_table(object_number):
    show_keys = ["object_number", "housing_area", "address", "accommodation_type",
                 "living_space", "monthly_rent", "valid_from", "end_date",
                 "application_ddl", "electricity_include", "rent_free_june_and_july",
                 "max_4_years"]
    apartment_info = ApartmentInfo.find_one({"object_number": object_number})
    table_html = """
    <div class="col-lg-12">
        <table class="table table-bordered table-hover">
           <caption>{}</caption>
           <thead>
              <tr>
                 <th>Item</th>
                 <th>Value</th>
              </tr>
           </thead>
           <tbody>
                """.format(apartment_info.name)
    for key, value in apartment_info.get_info().items():
        if key in show_keys:
            table_html += """
                  <tr>
                     <td>{}</td>
                     <td>{}</td>
                  </tr>
                    """.format(key, value)
    table_html += """ 
           </tbody>
        </table>
    </div>
                 """

    return table_html



def get_apartment_line(object_number):
    statuses = ApartmentStatus.find_many({"object_number": object_number})
    times = []
    queue_lens = []
    credits = []
    for status in statuses:
        times.append(status.get_update_time())
        queue_lens.append(status.queue_len)
        credits.append(status.most_credit)
    c = (
        Line(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add_xaxis(xaxis_data=times)
        .add_yaxis(
            series_name="Most credits",
            y_axis=credits,
            is_symbol_show=False,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                ]
            ),
        )
        .add_yaxis(
            series_name="Queue length",
            y_axis=queue_lens,
            is_symbol_show=False,
            yaxis_index=1,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                ]
            ),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
            name="Queue length",
            name_location="start",
            type_="value",
            max_=math.ceil(max(queue_lens) / 5) * 10,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Apartment Status", 
                                      subtitle=object_number),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name="Most credits", type_="value", 
                                     max_=math.ceil(max(credits) / 100) * 100,
                                     min_=max(math.floor(min(credits) / 100 - 1) * 100, 0)),
        )
    )
    return c

def get_regions():
    region_list = sorted(ApartmentInfo._collection.distinct("housing_area"))
    regions = [{"name": r} for r in region_list]
    return dict2obj(regions)

def get_types():
    type_list = sorted(ApartmentInfo._collection.distinct("accommodation_type"))
    types = [{"name": t} for t in type_list]
    return dict2obj(types)

def get_space_boundaries():
    active_apartments = ApartmentInfo.find_active_ones()
    space_list = [a.living_space for a in active_apartments if a.living_space is not None]
    if len(space_list) > 0:
        space_boundaries = {"min": min(space_list), "max": max(space_list)}
    else:
        space_boundaries = {"min": 0, "max": 0}
    return dict2obj(space_boundaries)


def get_rent_boundaries():
    active_apartments = ApartmentInfo.find_active_ones()
    rent_list = [a.monthly_rent for a in active_apartments if a.monthly_rent is not None]
    if len(rent_list) > 0:
        rent_boundaries = {"min": min(rent_list), "max": max(rent_list)}
    else:
        rent_boundaries = {"min": 0, "max": 0}
    return dict2obj(rent_boundaries)

def get_floor_boundaries():
    active_apartments = ApartmentInfo.find_active_ones()
    floor_list = [a.floor for a in active_apartments if a.floor is not None]
    if len(floor_list) > 0:
        floor_boundaries = {"min": min(floor_list), "max": max(floor_list)}
    else:
        floor_boundaries = {"min": 0, "max": 0}
    return dict2obj(floor_boundaries)

def dict2obj(args):
    """
    Convert dict to class object
    """
    class Obj(object):
        def __init__(self, d):
            for key, value in d.items():
                if isinstance(value, (list, tuple)):
                    setattr(self, key, 
                            [Obj(x) if isinstance(x, dict) else x for x in value])
                else:
                    setattr(self, key, Obj(value) if isinstance(value, dict) else value)
    if isinstance(args, (list, tuple)):
        return [dict2obj(o) for o in args]
    elif isinstance(args, dict):
        return Obj(args)
    else:
        return args
