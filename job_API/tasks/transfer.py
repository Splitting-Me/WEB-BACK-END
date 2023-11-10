# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import pydash as py_
from worker import worker
from models import UsersModel,PointsModel
from services.user import UserServices
from config import Config
from bson import Int64
from datetime import datetime, timedelta
@worker.task(name='worker.transfertoken', rate_limit='1000/s')
def transfertoken(event: str):
    args = py_.get(event,'args')
    _from = args['fromadd']
    _to = args['toadd']
    _tokens = args['ammount']
    _tokens = _tokens[:-18]
    _tokens = int(_tokens)
    _point = UserServices.convert_point(_tokens)
    _txhash = args['txhash']
    txhash = PointsModel.find({'txhash': _txhash})
    if txhash:
        return "txhash is exist"
    if _from == Config.AUTH_ADDRESS:
        # insert point for all user
        user = UsersModel.find_one({'user_address': _to})
        referral_list = list(user['referral_list'])
        insertdocument = []
        if len(referral_list) != 0:
            referral_list_points = list(PointsModel.find({'user_address': {'$in': referral_list},'deleted': False}))
            referral_list_user = list(UsersModel.find({'user_address': {'$in': referral_list}}))
            documents = PointsModel.find({'user_address': _to})
            total = UserServices.calculate_points(documents=documents)
            predirect = total
            prerank = UserServices.calculate_rank(total=total)
            total = total + _point
            rank = UserServices.calculate_rank(total=total)
            if rank > user['rank']:
                UsersModel.update_one({'user_address': _to},{'rank': rank,'updated_at': datetime.now(),'updated_by': _to})
       
            index = 0 
            for referral in referral_list:
                filtered_documents =[]
                for document in referral_list_points:
                    if document['user_address'] == referral and document['direct'] == True:
                        filtered_documents.append(document)
                #filtered_documents = [document for document in referral_list_points if document["user_address"] == referral and document["direct"] == True]
                totaldirect = UserServices.calculate_points(documents=filtered_documents)
                # if totaldirect >= predirect or referral['rank'] >= prerank:
                if totaldirect >= predirect:
                    predirect = totaldirect
                    filtered_documents =[]
                    for document in referral_list_points:
                        if document['user_address'] == referral:
                            filtered_documents.append(document)

                    #filtered_documents = [document for document in referral_list_points if referral_list_points["user_address"] == referral]
                    #filtered_user = [document for document in referral_list_user if referral_list_user["user_address"] == referral]
                    print(referral_list_user)
                    filtered_user=[]
                    for document in referral_list_user:
                        if document['user_address'] == referral:
                            filtered_user.append(document)
                    total = UserServices.calculate_points(documents=filtered_documents)
                    if total == 0: continue
                    rank = UserServices.calculate_rank(total=total)
                    
                    
                    if rank > filtered_user[0]['rank']:
                        UsersModel.update_one({'user_address': referral},{'rank': rank,'updated_at': datetime.now(),'updated_by': _to})
                    floor = UserServices.floor(rank=rank)
                    if floor >= index:
                        if index == 0:
                            insertdocument.append({'user_address': referral, 'point': round(_point/10), 'direct': True, 'created_at': datetime.now(),'created_by': _to,'deleted': False,'txhash': _txhash})
                        else:
                            insertdocument.append({'user_address': referral, 'point': round(_point/100), 'direct': False, 'created_at': datetime.now(),'created_by': _to,'deleted': False,'txhash': _txhash})
                index += 1
        insertdocument.append({'user_address': _to, 'point': _point, 'direct': True, 'created_at': datetime.now(),'created_by': _to,'deleted': False,'txhash': _txhash})
        print(insertdocument)
        PointsModel.insert_many(insertdocument)
        # check new rank for buyer 
      
        return "success"    
                

  
