from aiohttp import web
from marshmallow import Schema, fields, post_load

from ..db import models as db
from ..db.models.Team import Team
from ..serializers.team import TeamSchema

routes = web.RouteTableDef()

@routes.view("/team")
class TeamApi(web.View):
  schema = TeamSchema()

  async def get(self):
    qs = db.session.query(Team).all()
    return web.json_response(list(map(lambda m: self.schema.dump(m), qs)))

  async def post(self):
    data = await self.request.json()
    team = self.schema.load(data)

    try:
      session = db.DBSession()
      session.add(team)
      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(team))
