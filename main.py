from core import *
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType

global_theme = ThemeType.INFOGRAPHIC
# global_theme = ThemeType.LIGHT
# global_theme = ThemeType.WONDERLAND

table, index, items = read_excel(1)


def show_submit_time(table:pd.DataFrame, index):
    time_name = "提交答卷时间"
    time_stamp = [parse_time(i).int_timestamp for i in table[item_name]]
    time_24h = []
    for i in table[time_name]:
        t = parse_time(i).time()
        time_24h.append(t.hour + t.minute/60)

    return save_and_show(
        Grid(init_opts=get_init_options())
        .add(
            Scatter(init_opts=get_init_options())
            .add_xaxis(index)
            .add_yaxis("", time_stamp, symbol_size=4)
            .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在时间线上的分布"),
                yaxis_opts=opts.AxisOpts(is_scale=True, name="时间戳/ms"),
                xaxis_opts=opts.AxisOpts(name="答卷序号"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(False),
            ),
            opts.GridOpts(pos_left=0.5)
        )
        .add(
            Scatter(init_opts=get_init_options())
            .add_xaxis(index)
            .add_yaxis("", time_24h, symbol_size=4)
            .set_global_opts(
                title_opts=opts.TitleOpts(subtitle="散点图", title="提交时间在24h中的分布"),
                yaxis_opts=opts.AxisOpts(name="在一天中的时间/h"),
                xaxis_opts=opts.AxisOpts(name="答卷序号"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(False),
            ),
            opts.GridOpts(pos_right=0.5)
        ),
        "提交时间分布-散点图"
    )

def show_time_used(table:pd.DataFrame, index):
    item_name = "所用时间"
    item = [int(i[:-1]) for i in table[item_name]]
    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis(index)
        .add_yaxis("", item, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="做题用时的分布"),
            yaxis_opts=opts.AxisOpts(name="用时/s"),
            xaxis_opts=opts.AxisOpts(name="答卷序号"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        ),
        f"用时分布_散点图"
    )

def show_used_comp_submit(table):
    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis([int(i[:-1]) for i in table["所用时间"]])
        .add_yaxis("", [parse_time(i).int_timestamp for i in table["提交答卷时间"]], symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="用时与提交时间的关系"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/s"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="提交时间/ms"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        ),
        f"用时分布与提交时间的关系_散点图"
    )

def show_used_comp_submit_2(table):
    item = []
    for i in table["提交答卷时间"]:
        t = parse_time(i).time()
        item.append(t.hour + t.minute/60)
    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis([int(i[:-1]) for i in table["所用时间"]])
        .add_yaxis("", item, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="散点图", title="用时与提交时间的关系"),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="用时/s"),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="提交时间/ms"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        ),
        f"用时分布与提交时间的关系_散点图"
    )

def get_init_options(height=360):
    return opts.InitOpts(
        theme=global_theme,
        animation_opts=opts.AnimationOpts(bool(delay)),
        # width="1280px",
        height=f"{height}px",
    )
