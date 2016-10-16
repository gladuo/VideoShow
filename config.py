# coding=utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    SHOWS_PER_PAGE = 5
    VIDEOS_PER_PAGE = 5
    COMMENTS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
