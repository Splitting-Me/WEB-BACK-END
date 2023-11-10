# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel

__models__ = ['UsersModel', 'SessionsModel']

UsersModel = DaoModel(col=connect_db.db.users, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
PointsModel = DaoModel(col=connect_db.db.points, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
ReferralModel = DaoModel(col=connect_db.db.referral, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
