from aiohttp import web
from marshmallow import Schema, fields, post_load
from ..db import models as db
from ..db.models.Match import Match
from ..serializers.match import MatchRequestSchema, MatchResponseSchema

from .middlewares.auth import auth_required 
routes = web.RouteTableDef()


@routes.view("/match")
class MatchApi(web.View):
  request_schema = MatchRequestSchema()
  response_schema = MatchResponseSchema()

  async def get(self):
    qs = db.session.query(Match).all()
    return web.json_response(list(map(lambda m: self.response_schema.dump(m), qs)))

  @auth_required
  async def post(self):
    data = await self.request.json()
    match = self.request_schema.load(data)
    #match.state = MatchState.started
    match.firstSideT = 0
    match.firstSideCT = 0
    match.secondSideT = 0
    match.secondSideCT = 0
    match.firstSideTerrorist = 'A'
    match.mapSelectionMode = 'rng'

    try:
      session = db.DBSession()
      session.add(match)
      session.commit()
    except:
      session.rollback()
      raise

    return web.json_response(self.response_schema.dump(match))
