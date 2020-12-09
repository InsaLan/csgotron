from aiohttp import web
from  ..db.models.ApiUser import ApiUser
from marshmallow import Schema, fields

class ApiUserRequestSchema(Schema):
    id = fields.Int(required=True)
    token = fields.Str()

class ApiUserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()

class ApiUserCreateResponseSchema(Schema):
    token = fields.Str()

class ApiUserCreationSchema(Schema):
    username = fields.Str()
    password = fields.Str(required=True)