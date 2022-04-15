# -*- coding:utf-8 -*-
from flask import Blueprint, redirect, render_template, request, url_for
from app.ros.plot_elem import ShowItem, ShowBlock, ShowFigure
from app.manager.ros_manager import RosManager

bp = Blueprint("showlist", __name__)

show_example = """
# tof
/hal/sensor/cliff_with_odometry,CliffWithOdometryMSG,front_bottom_distance,front_bottom_distance

# 沿边psd
/hal/sensor/measure_with_odometry,MeasureWithOdometryMSG,side_distance,side_distance

# 探地
/hal/sensor/cliff_with_odometry,CliffWithOdometryMSG,cliff_lt,左前
/hal/sensor/cliff_with_odometry,CliffWithOdometryMSG,cliff_lb,左后
/hal/sensor/cliff_with_odometry,CliffWithOdometryMSG,cliff_rb,右后
/hal/sensor/cliff_with_odometry,CliffWithOdometryMSG,cliff_rt,右前

# imu
/hal/sensor/imu_with_odometry,ImuWithOdometryMSG,imu.roll,roll
/hal/sensor/imu_with_odometry,ImuWithOdometryMSG,imu.pitch,pitch
"""

@bp.route("/", methods=("GET", "POST"))
def showlist():
    """要展示的topic列表"""

    if request.method == "POST":
        showlist = request.form["showlist"]   
        show_figure = showlist_parse(showlist)
        ros_manager = RosManager()
        ros_manager.subscribe(show_figure)

        return redirect(url_for("databoard.databoard"))

    return render_template("showlist.html", show_example=show_example)


def showlist_parse(str):
    """展示topic列表内容解析"""
    figure = ShowFigure("Data")

    content = str.split('\n')
    for line in content:
        line = line.strip()
        if line == '':
            continue
        if line.startswith('#'):
            figure.show_blocks.append(ShowBlock(line[1:].strip()))
        else:
            line_content = line.split(',')
            if len(line_content) == 4:
                item = ShowItem(line_content[0], line_content[1], line_content[2], line_content[3])
                figure.show_blocks[-1].show_items.append(item)
    figure.print()
    
    return figure