# Create your views here.
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from datetime import date, datetime
import pymongo

import socket
hostname = socket.gethostname()

template_path = "/home/projects/SSSBReminder/SSSB/SSSB/templates"
if hostname == "xyz-ENVY-15":
    template_path = "/home/xyz/Documents/Projects/web_check/SSSBReminder/SSSB/SSSB/templates"

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader(template_path))


mongo_path = "mongodb://localhost:27017"
if hostname == "xyz-ENVY-15":
    mongo_path = "mongodb://localhost:1027"
client = pymongo.MongoClient(mongo_path)
db = client["SSSB"]
url_collection = db["apartment_url"]
info_collection = db["apartment_info"]
status_collection = db["apartment_status"]

def hello(request):

    urls = url_collection.find()
    times = []
    counts = []
    current_hour = None
    count = 0
    for url in urls:
        url_time = datetime.strptime(url["update_time"], "%Y-%m-%d %H:%M:%S")
        hour_time = datetime(year=url_time.year, 
                             month=url_time.month,
                             day=url_time.day,
                             hour=url_time.hour,
                             )
        if hour_time == current_hour:
            count += 1
        else:
            if current_hour is not None:
                times.append(current_hour.strftime("%Y-%m-%d %H:%M:%S"))
                counts.append(count)
            count = 1
            current_hour = hour_time
    
    c = (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=times)
        .add_yaxis(
            series_name="Number of available apartments",
            y_axis=counts,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
            #markline_opts=opts.MarkLineOpts(
            #    data=[opts.MarkLineItem(type_="average", name="平均值")]
            #),
        )
        #.add_yaxis(
        #    series_name="最低气温",
        #    y_axis=low_temperature,
        #    markpoint_opts=opts.MarkPointOpts(
        #        data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
        #    ),
        #    markline_opts=opts.MarkLineOpts(
        #        data=[
        #            opts.MarkLineItem(type_="average", name="平均值"),
        #            opts.MarkLineItem(symbol="none", x="90%", y="max"),
        #            opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
        #        ]
        #    ),
        #)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="SSSB展示", subtitle="测试"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return HttpResponse(c.render_embed())

