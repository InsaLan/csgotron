from aiohttp import web
from ..db.models.Server import Server
from marshmallow import Schema, fields, post_load


class ServerSchema(Schema):
<<<<<<< HEAD
  id = fields.Int(dump_only=True)
=======
  id = fields.Int()
>>>>>>> 682c9c8 ([feat] start ApiUser)
  ip = fields.IPv4()
  port = fields.Int()
  nickname = fields.Str()

  @post_load
  def make_server(self, data, **kwargs):
    return Server(**data)

