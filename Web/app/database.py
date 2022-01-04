# -*- conding:utf-8 -*-
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """连接数据库"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """创建数据库"""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    """命令行创建数据库"""
    init_db()
    click.echo("初始化数据库")

def init_app(app):
    """注册到app时调用"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)