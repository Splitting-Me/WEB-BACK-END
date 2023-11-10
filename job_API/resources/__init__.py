from resources.health_check import HealthCheck
from resources.user import UserResource
from resources.referral import ReferralResource
from resources.ipfs import IpfsServiceResource
# from resources.iapi import iapi_resources
api_resources = {
    '/common/health_check': HealthCheck,
    '/user/<string:user_address>':UserResource,
    '/referral':ReferralResource,
    '/ipfs':IpfsServiceResource,
    # **{f'/iapi{k}': val for k, val in iapi_resources.items()},

}

