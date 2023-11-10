from flask_restful import Resource
from connect import security
from pydash import get
import pydash as py_
from services.ipfs import IpfsService
from schemas.schemas import IpfsSchema,IpfsResponseSchema
class IpfsServiceResource(Resource):
    @security.http(
            form_data=IpfsSchema(),
            response=IpfsResponseSchema(),
            login_required=False,
        )
    def post(self,form_data):
        url = IpfsService.ipfs_generator(form_data=form_data)
        return url