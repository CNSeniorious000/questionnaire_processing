import enum
import arrow
import threading
import pandas as pd
from selenium import webdriver
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def read_excel(path):
    table = pd.read_excel(rf"data\{path}.xlsx", engine="openpyxl")
    index = list(table["序号"])
    items = list(table.columns)
    return table, index, items

def parse_time(string):
    date, time = string.split()
    return arrow.get(f"{date} {('0'+time)[-8:]}")

class Driver(enum.Enum):
    Edge = enum.auto()
    Firefox = enum.auto()
    Chrome = enum.auto()

def to_png(html, name, ratio=3, delay=0, driver=Driver.Edge, remove=False):
    match driver:
        case Driver.Edge:
            options = EdgeOptions()
            options.add_argument("headless")
            driver = webdriver.Edge(options=options)
            make_snapshot(snapshot, html, rf"output\{name}.png", delay, ratio, remove, driver=driver)
            driver.quit()

        case Driver.Firefox:
            options = FirefoxOptions()
            options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)
            make_snapshot(snapshot, html, rf"output\{name}.png", delay, ratio, remove, driver=driver)
            driver.quit()

        case Driver.Chrome:
            make_snapshot(snapshot, html, rf"output\{name}.png", delay, ratio, remove)

delay = 0

def save_and_show(plot, name, ratio=3, delay=delay, driver=Driver.Edge, remove=True, multithreading=True):
    args = (plot.render(), name, ratio, delay, driver, remove)
    threading.Thread(target=to_png, args=args).start() if multithreading else to_png(*args)
    return plot.render_notebook()


# project specific staffs ##########################################################

from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType
global_theme = ThemeType.INFOGRAPHIC


def show_submit_time(table:pd.DataFrame, index):
    item_name = "提交答卷时间"
    item = [parse_time(i).int_timestamp for i in table[item_name]]

    return save_and_show(
        Scatter(init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(bool(delay), animation_duration=1000*delay),
            theme=global_theme,
            # width="1280px",
            height="360px",
        ))
        .add_xaxis(index)
        .add_yaxis(item_name, item, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="散点图"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="时间戳/ms"),
            xaxis_opts=opts.AxisOpts(name="答卷序号"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        ),
        f"提交时间分布_散点图"
    )

