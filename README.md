# RobotVisualize
机器人可视化套件

## Web
云端数据处理，可视化。

python3 -m venv venv
. venv/bin/activate
pip install Flask
pip install pyecharts

export FLASK_APP=app
export FLASK_ENV=development
flask init-db
flask run --host=127.0.0.1