# -*- coding:utf-8 -*-
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key'
    DATABASE = os.path.join(BASEDIR, '../db.sqlite')

class DevelopmentConfig(Config):
    """测试配置"""
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or + os.path.join(BASEDIR, 'data.sqlite')

class ProductConfig(Config):
    """生产配置"""
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or + os.path.join(BASEDIR, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'product': ProductConfig
}