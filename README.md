# RobotVisualize
机器人可视化套件

## Robot
运行于机器人上，作为TCP客户端收集数据，上传至服务器端。

## Web
云端数据处理，可视化。

1.server告诉client需要上传的数据

python3 -m venv venv
. venv/bin/activate
pip install Flask
export FLASK_APP=app
export FLASK_ENV=development
flask init-db
flask run --host=127.0.0.1