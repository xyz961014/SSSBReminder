# Create your views here.
from django.http import HttpResponse
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

    input_area = """
   <head>
      <title>SSSB统计</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
   </head>
   <body>
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
   </body>
                 """
    page = Page(layout=Page.SimplePageLayout)
    amount_line = get_amount_line()
    object_number = request.GET.get("object_number", None)
    if object_number is not None:
        object_line = get_apartment_line(object_number)
        page.add(
            amount_line,
            object_line
                )
    else:
        page.add(
            amount_line,
                )
    return HttpResponse(input_area + page.render_embed())



# Charts

def get_amount_line():
    amounts = ApartmentAmount.find_many()
    times = []
    counts = []
    for amount in amounts:
        times.append(amount.update_time)
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

def get_apartment_line(object_number):
    statuses = ApartmentStatus.find_many({"object_number": object_number})
    times = []
    queue_lens = []
    credits = []
    for status in statuses:
        times.append(status.update_time)
        queue_lens.append(status.queue_len)
        credits.append(status.most_credit)
    c = (
        Line(init_opts=opts.InitOpts())
        .add_xaxis(xaxis_data=times)
        .add_yaxis(
            series_name="Most credits",
            y_axis=credits,
            is_symbol_show=False,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
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
                                     max_=math.ceil(max(credits) / 100) * 100),
        )
    )
    return c


