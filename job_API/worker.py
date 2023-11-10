# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sentry_sdk
from celery import Celery
from flask import Flask
from config import Config
from connect import connect_db


def create_worker():
    app = Flask(__name__)
    connect_db.init_app(app, Config.MONGO_URI)
    _celery = Celery(__name__, broker=Config.BROKER_URL)
    _celery.conf.update(
        CELERY_IMPORTS =['tasks'],
        ENABLE_UTC =True,
        BROKER_USE_SSL =True
    )

 

    return _celery


# init connect db


worker = create_worker()
