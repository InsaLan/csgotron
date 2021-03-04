from . import EventHandler
from src.db import models as db
from src.db.models.Match import Match
from src.db.models.Player import Player
import logging

class EnteredGameEventHandler(EventHandler):
  def __init__(self,
               player_name: str,
               player_uid: int,
               player_steam_id: str):
    EventHandler.__init__(self)
    self.player_name = player_name
    self.player_uid = player_uid
    self.player_steam_id = player_steam_id
    self.logger = logging.getLogger(__name__)

  def handle(self, match: Match):
    is_bot = False

    if self.player_steam_id == 'BOT':
      self.player_steam_id = match.id * 1000 + self.player_uid
      is_bot = True

    self.logger.debug("Handling EnteredGame event for player {} (id = {})".format(self.player_name, self.player_steam_id))

    if not self.session.query(Player).filter(Player.id == self.player_steam_id).count() > 0:
      pl = Player(id=self.player_steam_id, username =self.player_name, isBot=is_bot)
      self.session.add(pl)
      self.session.commit()
