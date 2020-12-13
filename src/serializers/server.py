from aiohttp import web
from ..db.models.Server import Server
from marshmallow import Schema, fields, post_load


class ServerSchema(Schema):
<<<<<<< HEAD
<<<<<<< HEAD
  id = fields.Int(dump_only=True)
=======
  id = fields.Int()
>>>>>>> 682c9c8 ([feat] start ApiUser)
=======
  id = fields.Int()
>>>>>>> 682c9c8c09640026f46c9a5adf69f66d9fdb7a19
  ip = fields.IPv4()
  port = fields.Int()
  nickname = fields.Str()

  @post_load
  def make_server(self, data, **kwargs):
    return Server(**data)

