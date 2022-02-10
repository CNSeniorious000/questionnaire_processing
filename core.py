import enum
import arrow
import threading
import pandas as pd
from selenium import webdriver
from snapshot_selenium import snapshot
from loky import get_reusable_executor
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

delay = 1

def save_and_show(plot, name, ratio=3, delay=delay, driver=Driver.Edge, remove=True, concurrent="thread"):
    args = (plot.render(f"{name}.html"), name, ratio, delay, driver, remove)
    match concurrent:
        case "loky": get_reusable_executor(max_workers=16, reuse=True).submit(to_png, *args)
        case "thread": threading.Thread(target=to_png, args=args).start()
        case _: to_png(*args)
    return plot.render_notebook()
