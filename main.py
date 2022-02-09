from core import *
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType

global_theme = ThemeType.INFOGRAPHIC

def get_init_options(height=360):
    return opts.InitOpts(
        theme=global_theme,
        animation_opts=opts.AnimationOpts(bool(delay)),
        # width="1280px",
        height=f"{height}px",
    )

def show_submit_time(table:pd.DataFrame, index):
    item_name = "提交答卷时间"
    item = [parse_time(i).int_timestamp for i in table[item_name]]
    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis(index)
        .add_yaxis("答卷", item, symbol_size=4)
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

def show_time_used(table:pd.DataFrame, index):
    item_name = "所用时间"
    item = [int(i[:-1]) for i in table[item_name]]
    return save_and_show(
        Scatter(init_opts=get_init_options())
        .add_xaxis(index)
        .add_yaxis("答卷", item, symbol_size=4)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="散点图"),
            yaxis_opts=opts.AxisOpts(name="用时/s"),
            xaxis_opts=opts.AxisOpts(name="答卷序号"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(False),
        ),
        f"用时分布_散点图", multithreading=False
    )
