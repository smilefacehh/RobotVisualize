# -*- coding:utf-8 -*-
from datetime import datetime
from sys import stderr
from flask import Blueprint, redirect, render_template, request, url_for
from flask.json import jsonify
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
from app.ros.plot_elem import ShowItem, ShowBlock, ShowFigure
from app.manager.ros_manager import RosManager

bp = Blueprint("databoard", __name__)
ros_manager = RosManager()

color = ['blue','cyan','green','red','darkorange','magenta','olive','black']

@bp.route("/databoard/", methods=("GET", "POST"), endpoint="databoard")
def databoard():
    """展示数据"""
    n_block = ros_manager.get_block_num()
    print("block num %d" % n_block, file=stderr)
    return render_template("databoard.html", n_block=n_block)


def line_base(block_title, item_labels) -> Line:
    lineVol = Line(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
    lineVol.add_xaxis([])
    for i in range(len(item_labels)):
        lineVol.add_yaxis(series_name=item_labels[i],y_axis=[],color=color[i],label_opts=opts.LabelOpts(is_show=False),)
        lineVol.set_global_opts(
            title_opts=opts.TitleOpts(title=block_title, pos_top="3%"),
            legend_opts=opts.LegendOpts(pos_top="5%"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross", trigger="axis"),
            datazoom_opts=opts.DataZoomOpts(type_="slider"),
            xaxis_opts=opts.AxisOpts(name='time'),
            yaxis_opts=opts.AxisOpts(type_='value',name='value',splitline_opts=opts.SplitLineOpts(is_show=True),is_scale=True),)
 
    return lineVol


@bp.route("/base_line/<int:block_id>/")
def get_line_chart(block_id):
    print(block_id, file=stderr)
    if len(ros_manager.show_figure.show_blocks) > block_id:
        block_title = ros_manager.show_figure.show_blocks[block_id].block_title
        item_labels = []
        for item in ros_manager.show_figure.show_blocks[block_id].show_items:
            item_labels.append(item.show_label)
        print(block_title, file=stderr)
        print(item_labels, file=stderr)
        c = line_base(block_title=block_title, item_labels=item_labels)
        return c.dump_options_with_quotes()
    return jsonify({})


@bp.route("/figure_size/")
def get_figure_size():
    """
    {
        'fig_size': [4, 2]
    }
    """
    fig_size = ros_manager.get_figure_size()
    print(fig_size, file=stderr)
    return jsonify({"fig_size": fig_size})


@bp.route("/dynamic_data/")
def update_line_data():
    """
    {
        'x_time': 16:20:34
        'y': [
            [1,2,3,4],
            [1,2]
        ]
    }
    """
    y = ros_manager.get_data()
    print(y, file=stderr)
    return jsonify({"x_time": datetime.now().strftime("%H:%M:%S"), "y": y})