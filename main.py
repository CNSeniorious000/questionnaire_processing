from core import *
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# global_theme = ThemeType.INFOGRAPHIC
# global_theme = ThemeType.LIGHT
global_theme = ThemeType.WONDERLAND


table, index, items = read_excel(1)

time_stamp = [parse_time(i).int_timestamp / 1000 / 60 for i in table["提交答卷时间"]]
time_24h = []
for i in table["提交答卷时间"]:
    t = parse_time(i).time()
    time_24h.append(t.hour + t.minute / 60)

def show_submit_time():
    return save_and_show(
        Grid(get_init_options())
        .add(
            Scatter(init_opts=get_init_options())
            .add_xaxis(index)
            .add_yaxis("", time_stamp, symbol_size=4)
            .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在时间线上的分布"),
                yaxis_opts=opts.AxisOpts(is_scale=True, name="时间戳/min"),
                xaxis_opts=opts.AxisOpts(name="答卷序号"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(False),
            ),
            opts.GridOpts(pos_right="56%")
        )
        .add(
            Scatter(init_opts=get_init_options())
            .add_xaxis(index)
            .add_yaxis("", time_24h, symbol_size=4)
            .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在24h的分布", pos_left="46%"),
                yaxis_opts=opts.AxisOpts(name="时刻/h"),
                xaxis_opts=opts.AxisOpts(name="答卷序号"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(False),
            ),
            opts.GridOpts(pos_left="56%")
        ),
        "提交时间分布-散点图"
    )

time_cost = [int(i[:-1]) for i in table["所用时间"]]

def show_time_used():
    y = [0] * (4 * 6 + 1)
    for i in time_cost:
        y[min(i // 15, 24)] += 1
    return save_and_show(
        Bar(get_init_options())
        .add_xaxis([f"{i / 4}" for i in range(24)] + ["6+"])
        .add_yaxis("", y)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="柱状图", title="填写答卷用时分布"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/min"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="人数/人"),
        ),
        f"用时分布_条形图"
    )

def show_used_comp_submit_2():
    x, y = zip(*sorted(zip(time_cost, time_24h)))

    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis(x)
        .add_yaxis("", y, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="用时与提交时间的关系"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/s"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="提交时间/ms"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        )
        ,
        f"用时分布与提交时间的关系_散点图"
    )

def get_init_options(height=360):
    return opts.InitOpts(
        theme=global_theme,
        animation_opts=opts.AnimationOpts(bool(delay)),
        # width="1280px",
        height=f"{height}px"
    )
