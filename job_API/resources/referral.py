from flask_restful import Resource
from connect import security
from pydash import get
import pydash as py_

from services.referral import ReferralServices
from schemas.schemas import ReferralSchema
class ReferralResource(Resource):
    @security.http(
            params=ReferralSchema(),
            login_required=False,
        )
    def get(self,params):
        message = ReferralServices.get_sign_message(self,params=params)
        return message

    @security.http(
        form_data=ReferralSchema(),
        login_required=False,
    )
    def put(self,form_data):
        _point = ReferralServices.referral(form_data=form_data)
        return _point