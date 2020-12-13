from aiohttp import web
from  ..db.models.ApiUser import ApiUser
from marshmallow import Schema, fields, post_load

class ApiUserRequestSchema(Schema):
    id = fields.Int(required=True)
    token = fields.Str()

class ApiUserAuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ApiUserTokenResponseSchema(Schema):
    token = fields.Str()

class ApiUserCreationSchema(Schema):
    username = fields.Str()
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return ApiUser(**data)