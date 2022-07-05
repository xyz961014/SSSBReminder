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

from datetime import date, datetime
import math
import pymongo

import os
import sys
curr_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(curr_path, "../.."))
from sssb_item import ApartmentInfo, ApartmentURL, ApartmentStatus, ApartmentAmount

import socket
hostname = socket.gethostname()

template_path = "/home/projects/SSSBReminder/SSSB/SSSB/templates"
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

def index(request):
    data = {
            "region_list": get_regions(),
            "type_list": get_types(),
            "space_boundaries": get_space_boundaries(),
            "rent_boundaries": get_rent_boundaries(),
            }
    return render(request, "index.html", data)

def available_apartments(request):
    #page = Page(layout=Page.SimplePageLayout)
    amount_line = get_amount_line()
    #page.add(
    #    amount_line,
    #        )
    return HttpResponse(amount_line.render_embed())


def apartment_status(request):

    input_area = """
   <head>
      <title>SSSB统计</title>
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
    space_list = sorted([a.living_space for a in active_apartments])
    space_boundaries = {"min": space_list[0], "max": space_list[-1]}
    return dict2obj(space_boundaries)


def get_rent_boundaries():
    active_apartments = ApartmentInfo.find_active_ones()
    rent_list = sorted([a.monthly_rent for a in active_apartments])
    rent_boundaries = {"min": rent_list[0], "max": rent_list[-1]}
    return dict2obj(rent_boundaries)

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
                    setattr(self, key, Obj(b) if isinstance(value, dict) else value)
    if isinstance(args, (list, tuple)):
        return [dict2obj(o) for o in args]
    elif isinstance(args, dict):
        return Obj(args)
    else:
        raise TypeError("Must convert list, tuple or dict.")
