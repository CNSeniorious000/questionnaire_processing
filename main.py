from collections import Counter
from core import *
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# global_theme = ThemeType.INFOGRAPHIC
# global_theme = ThemeType.LIGHT
# global_theme = ThemeType.WONDERLAND
global_theme = ThemeType.ESSOS

all_plots = []

def get_init_options(height=360):
    return opts.InitOpts(
        theme=global_theme,
        animation_opts=opts.AnimationOpts(bool(delay)),
        # width="1280px",
        height=f"{height}px"
    )


table, index, items = read_excel(1)

def question(n):
    return items[n + 6 - 1]  # natural index

time_stamp = [parse_time(i).int_timestamp / 1000 / 60 for i in table["提交答卷时间"]]
time_24h = []
for i in table["提交答卷时间"]:
    t = parse_time(i).time()
    time_24h.append(t.hour + t.minute / 60)

def show_submit_time():
    s1 = (
        Scatter(get_init_options())
        .add_xaxis(index)
        .add_yaxis("", time_stamp, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在时间线上的分布"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="时间戳/min"),
            xaxis_opts=opts.AxisOpts(name="答卷序号"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(False))
    )
    s2 = (
        Scatter(get_init_options())
        .add_xaxis(index)
        .add_yaxis("", time_24h, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在24h的分布"),
            yaxis_opts=opts.AxisOpts(name="时刻/h"),
            xaxis_opts=opts.AxisOpts(name="答卷序号"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(False))
    )

    all_plots.append(s1)
    all_plots.append(s2)

    return save_and_show(Page(Page.SimplePageLayout).add(s1, s2), "提交时间分布-散点图")

time_cost = [int(i[:-1]) for i in table["所用时间"]]

def show_time_used():
    y = [0] * (4 * 6 + 1)
    for i in time_cost:
        y[min(i // 15, 24)] += 1

    bar = (
        Bar(get_init_options())
        .add_xaxis([f"{i / 4}" for i in range(24)] + ["6+"])
        .add_yaxis("", y)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="柱状图", title="填写答卷用时分布"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/min"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="人数/人"),
        )
    )

    all_plots.append(bar)

    return save_and_show(bar, "用时分布_柱状图", driver=Driver.Chrome)

def show_time_compare():
    x, y = zip(*sorted(zip(time_cost, time_24h)))

    scatter = (
        Scatter(init_opts=get_init_options())
        .add_xaxis(x)
        .add_yaxis("", y, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="用时与提交时间的关系"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/s"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="提交时间/ms"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(False))
    )

    all_plots.append(scatter)

    return save_and_show(scatter, f"用时分布与提交时间的关系_散点图")

def count(sequence):
    return sorted(Counter(sequence).items(), key=lambda i:i[1], reverse=True)

province_ip, city_ip = zip(*(i[i.index('(')+1:-1].split('-') for i in table["来自IP"]))
province_ans, city_ans = zip(*(i.split('-') for i in table["2、您所在的城市是【选填】"] if i != '(空)'))

def show_district(use_ip=False):
    if use_ip:
        province = province_ip
        city = city_ip
    else:
        province = province_ans
        city = city_ans

    x, y = zip(*count(province))

    bar = (
        Bar(get_init_options())
        .add_xaxis(x)
        .add_yaxis("", y)
        .set_global_opts(title_opts=opts.TitleOpts(subtitle="柱状图", title="来源地区-省"))
    )
    cloud = (
        WordCloud(get_init_options())
        .add("", count(city), word_size_range=(20, 30))
        .set_global_opts(title_opts=opts.TitleOpts(subtitle="词云图", title="来源地区-市"))
    )

    all_plots.append(bar)
    all_plots.append(cloud)

    return save_and_show(Page(Page.SimplePageLayout).add(bar, cloud), "来源地区_词云图")

