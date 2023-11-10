from flask_restful import Resource
from schemas.schemas import ResponseUserSchmas
from connect import security
from services.user import UserServices
class UserResource(Resource):

    @security.http(
        # login_required=True
        response=ResponseUserSchmas(),   
    )
    def get(self,user_address):
        print(user_address)
        user= UserServices.get_user(user_address=user_address)
        print(user)
        return user
    
    @security.http(
        # login_required=True   
    )
    def post(self,user_address):
        if(user_address == '0x00'):
            print('reset rank')
            UserServices.rank_reset()
        return {}
    