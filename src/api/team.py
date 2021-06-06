from aiohttp import web
from marshmallow import Schema, fields, post_load
from . import common
from src.db import models as db
from src.db.models.Team import Team
from src.serializers.team import TeamSchema
from src.api.middlewares.auth import auth_required 

routes = web.RouteTableDef()

@routes.view("/team")
class TeamApi(web.View):
  schema = TeamSchema()
  
  async def get(self):
    session = db.DBSession()
    qs = session.query(Team).all()
    return web.json_response(self.schema.dump(qs, many=True))

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

@routes.view("/team/{id}")
class TeamDetailsApi(common.DetailsApi):
  schema = TeamSchema()
  
  async def get(self):
    _id = await self.get_object_id()

    session = db.DBSession()
    team = session.query(Team).filter(Team.id == _id).one()
    return web.json_response(self.schema.dump(team))

  async def patch(self):
    _id = await self.get_object_id()
    data = await self.request.json()

    # HACK: exactly the same thing as schema.validate (validate against marshmallow without serializing)
    # but directly raise marshmallow ValidationError instead of returning a dict of validation errors
    self.schema._do_load(data, partial=True, postprocess=False)

    try:
      session = db.DBSession()
      team = session.query(Team).filter(Team.id == _id).one()
      common.patch_object(team, data)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.schema.dump(team))

  
  @auth_required
  async def delete(self):
    _id = await self.get_object_id()

    try:
      session = db.DBSession()
      team = session.query(Team).filter(Team.id == _id).one()
      session.delete(team)

      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response({"success": "the team has been deleted"}, status=200)
