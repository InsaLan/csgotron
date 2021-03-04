from . import EventHandler
from src.db import models as db
from src.db.models.Match import Match
from src.db.models.Round import Round
import logging

class RoundStartEventHandler(EventHandler):
  def __init__(self):
    EventHandler.__init__(self)
    self.logger = logging.getLogger(__name__)
  
  def handle(self, match: Match):

    self.logger.debug("Handling RoundStart event for match {}".format(match.id))
 
    i = self.get_current_round_id(match.id)
    if i == None:
      i = 1 

    r = Round(id=i, matchId=match.id)
    self.session.add(r)
    self.session.commit()
