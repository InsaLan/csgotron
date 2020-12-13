from aiohttp import web
from  ..db.models.ApiUser import ApiUser
<<<<<<< HEAD
from marshmallow import Schema, fields, post_load
=======
from marshmallow import Schema, fields
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19

class ApiUserRequestSchema(Schema):
    id = fields.Int(required=True)
    token = fields.Str()

<<<<<<< HEAD
class ApiUserAuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ApiUserTokenResponseSchema(Schema):
=======
class ApiUserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()

class ApiUserCreateResponseSchema(Schema):
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19
    token = fields.Str()

class ApiUserCreationSchema(Schema):
    username = fields.Str()
<<<<<<< HEAD
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return ApiUser(**data)
=======
    password = fields.Str(required=True)
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19
