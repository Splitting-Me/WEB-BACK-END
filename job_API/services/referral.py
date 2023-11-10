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
from models import UsersModel,PointsModel,ReferralModel
from helper.wallet import WalletHelper
from exceptions.referral import InvalidNonce,InvalidSignature

class ReferralServices():
    @staticmethod
    def validate_nonce(_nonce):
        _dt = dt_utcnow().timestamp() - _nonce
        print(_dt)
        if 360 >= _dt >= 0:
            return True

        return False
    @classmethod
    def referral(cls,form_data):

        user_address = py_.get(form_data,'user_address')
        if UsersModel.find_one({'user_address': user_address}):
            return {}
        _nonce = py_.get(form_data,'nonce')
        if not cls.validate_nonce(_nonce): 
            raise InvalidNonce('nonce invalid')
        signature = py_.get(form_data,'signature')
        _message = WalletHelper._get_sign_msg(user_address, _nonce)
        if len(signature)!= 132:
            raise InvalidSignature('signature invalid')
        _signer = WalletHelper.get_address_of(signature,_message)
        if _signer == user_address:
            referral_address = py_.get(form_data,'referral_address')
            if len(referral_address)!=42:
                referral_address= 'wrong'
            referral = UsersModel.find_one({'user_address': referral_address})
            if referral:
                referral_list = referral['referral_list']
                if len(referral_list)>15:
                    referral_list.pop()
            else:
                referral_list = []
            if user_address != referral_address:
                UsersModel.insert_one({
                    'user_address': user_address,
                    'referral_list': [referral_address]+referral_list,
                    'created_at': datetime.now(),
                    'created_by': referral_address,
                    'rank': 0,
                })
            return{}
        raise InvalidSignature('signature invalid')
    @staticmethod
    def get_sign_message(cls,params):
        _address = py_.get(params,'user_address')
        if not _address:
            return
        _message,_nonce = WalletHelper.get_sign_msg(_address)
        return {"message":_message,
                "address": _address,
                "nonce":_nonce}