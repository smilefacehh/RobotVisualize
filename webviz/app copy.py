import os
from sys import stderr
import threading
from datetime import datetime
from flask.json import jsonify
from flask import Flask, render_template, request, jsonify
 
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

app = Flask(__name__, static_folder="static",template_folder='templates')

color = ['blue','cyan','green','red','darkorange','magenta','olive','black']
 
def line_base() -> Line:
 
    lineVol = Line(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
    lineVol.add_xaxis([])
    for i in range(4):
        lineVol.add_yaxis(series_name="Thread"+str(i),y_axis=[],color=color[i],label_opts=opts.LabelOpts(is_show=False),)
    lineVol.set_global_opts(
            title_opts=opts.TitleOpts(title="Test", pos_top="3%"),
            legend_opts=opts.LegendOpts(pos_top="5%"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True, axis_pointer_type="cross", trigger="axis"),
            #datazoom_opts=opts.DataZoomOpts(type_="slider"),
            xaxis_opts=opts.AxisOpts(name='time'),
            yaxis_opts=opts.AxisOpts(type_='value',name='Volume',splitline_opts=opts.SplitLineOpts(is_show=True),is_scale=True),)
 
    return lineVol

@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()
 
@app.route("/lineDynamicData1")
def update_line_data():
    return jsonify({"xTime": datetime.now().strftime("%H:%M:%S"), "yValue": [1,2,3,4]})

@app.route("/lineDynamicData2")
def update_line_data2():
    return jsonify({"xTime": datetime.now().strftime("%H:%M:%S"), "yValue": [1,2,3,4]})


from app.tool import adbtool, netool, rostool

@app.route('/client/list/', methods=('GET', 'POST'))
def client_list():
    """机器人列表"""
    devices = netool.lan_devices()
    host_ip = netool.host_ip()
    selected_ip = '--选择--'
    ros_online = False

    if request.method == 'POST':
        selected_ip = request.values.get('select_ip')
        if netool.valid_ip(selected_ip):
            ros_online = True

    return render_template("index.html", devices=devices, host_ip=host_ip, selected_ip=selected_ip, ros_online=ros_online)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False)