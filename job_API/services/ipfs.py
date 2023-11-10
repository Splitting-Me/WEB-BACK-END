import datetime
import traceback
import pydash as py_
import bson
from bson import ObjectId
from pymongo import MongoClient
import requests
from config import Config
import base64


# from lib import dt_utcnow
from lib.utils import util_web3, dt_utcnow
from datetime import datetime, timedelta
from connect import redis_cluster
from worker import worker
class IpfsService():
    @classmethod
    def ipfs_generator(cls,form_data):
        imagebase64 = py_.get(form_data,'image')
        image = base64.b64decode(imagebase64)
        name = py_.get(form_data,'name')
        description = py_.get(form_data,'description')
        data = image
        image_cid = cls.ipfs_call_nftstorage(data=data)
        print(image_cid)
        metadata = {'name': name,'description': description,'image': f'https://{image_cid}.ipfs.nftstorage.link/'}
        metadata = bson.json_util.dumps(metadata)
        url = cls.ipfs_call_nftstorage(data=metadata)
        url = {'url':f'https://{url}.ipfs.nftstorage.link/'}
        print(url)
        return url
    
    @staticmethod
    def ipfs_call_nftstorage(data):
        url = "https://api.nft.storage/upload"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDNGNmFBRTBkNWMyNDIxMTFiRWQzNkQxOTViNGFjNTA1RDI0MGQzRjgiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5NDEwMTA5MDQzMiwibmFtZSI6InNwbGl0dGluZ21lIn0.kkpJGDwoahuHfjveI9FcY-3tZs9afLawo4vXstK_2Z0",
            "Content-Type": "*/*",
        }
        response = requests.post(url, headers=headers, data=data)
        response = response.json()
        cid = response['value']['cid']
        return cid

        