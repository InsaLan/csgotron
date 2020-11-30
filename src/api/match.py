from aiohttp import web
from ..db import models as db
from ..db.models.Match import Match

routes = web.RouteTableDef()

@routes.view("/match")
class MatchApi(web.View):
  async def get(self):
    qs = db.session.query(Match).all()
    return web.json_response(qs)
