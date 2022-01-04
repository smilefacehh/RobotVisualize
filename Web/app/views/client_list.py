# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, flash, request, jsonify
from app.net import ip, tcp_client
import time

TCP_PORT=10002

bp = Blueprint('client_list', __name__, url_prefix='/')

@bp.route('/client/list/', methods=('GET', 'POST'))
def show_list():
    """机器人列表"""
    print(1)
    devices = ip.lan_devices()
    host_ip = ip.host_ip()
    selected_ip = '--选择--'
    connect_result = ''

    if request.method == 'POST':
        selected_ip = request.values.get('select_ip')
        print(selected_ip)
        if ip.valid_ip(selected_ip):
            connect_result = '正在连接'
            client = tcp_client.TcpClient(selected_ip, TCP_PORT)

            t = time.time()
            while True:
                if client.ok():
                    connect_result = '连接成功'
                    return render_template('test.html', content='')

                if time.time() - t > 3:
                    connect_result = '连接失败'
                    break

        else:
            connect_result = '请重新选择'


    return render_template('client_list.html', devices=devices, host_ip=host_ip, selected_ip=selected_ip, connect_result=connect_result)


@bp.route('/client/msg/', methods=('GET', 'POST'))
def show_client_msg():
    """显示来自client的消息"""
    content = 'default'
    if request.method == 'POST':
        content = request.values.get('msg')
        print(content)

    return render_template('test.html', content=content)