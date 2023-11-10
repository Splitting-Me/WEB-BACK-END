import datetime
import traceback
import pydash as py_
import bson
from bson import ObjectId
from pymongo import MongoClient

# from lib import dt_utcnow
from lib.utils import util_web3, dt_utcnow
from datetime import datetime, timedelta
from connect import redis_cluster
from worker import worker
from models import UsersModel,PointsModel
class UserServices():
    @classmethod
    def get_user(cls,user_address):
        
        documents = list(PointsModel.find({'user_address': user_address,'deleted': False}))
        total = cls.calculate_points(documents=documents)
        rank = UsersModel.find_one({'user_address': user_address})['rank']
        return { 'rank': rank, 'total': total }

    @staticmethod
    def calculate_rank(total):
        thresholds = [10000000, 1000000, 500000, 200000, 100000, 50000, 20000, 6000, 100]
        ranks = [9, 8, 7, 6, 5, 4, 3, 2, 1]

        for threshold, rank in zip(thresholds, ranks):
            if total >= threshold:
                return rank
        return 0

    @staticmethod
    def calculate_points(documents):
        total = 0
        for document in documents:
            total += document['point']
        return total
    
    @staticmethod
    def floor(rank):
        thresholds = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        floor = [14 ,11, 11 ,9 , 9, 7, 7, 5, 5]
        for threshold, floor in zip(thresholds, floor):
            if rank == threshold:
                return floor
        return 0

    @classmethod
    def rank_reset(cls):
        user_list = list(UsersModel.find({}))
        for user in user_list:
            print(user['updated_at'])
            if user['updated_at'] < datetime.now():
                PointsModel.update_many({'user_address': user['user_address']},{'deleted': True,'updated_at': datetime.now(),'updated_by': '0x00'})

    @staticmethod
    def convert_point(tokens):
        thresholds = [ 1010101, 452261, 200400, 100100, 10000]
        point = [10000, 4500, 2000, 1000, 100]
        for threshold, point in zip(thresholds, point):
            if tokens >= threshold:
                return point
        return 0        




    

