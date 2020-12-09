from aiohttp import web
from ..db import models as db
from ..db.models.ApiUser import ApiUser
from ..serializers.ApiUser import ApiUserCreateResponseSchema, ApiUserCreationSchema, ApiUserRequestSchema, ApiUserResponseSchema
routes = web.RouteTableDef()

@routes.view("/user")
class UserApi(web.view):
    creation_request_schema = ApiUserCreationSchema()
    creation_response_schema = ApiUserCreateResponseSchema()
    
    async def get(self):
        pass
    
    async def post(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass