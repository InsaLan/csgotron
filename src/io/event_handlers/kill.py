import logging
from typing import Tuple

from . import EventHandler
from src.db import models as db
from src.db.models.Match import Match
from src.db.models.Player import Player
from src.db.models.Kill import Kill
from src.exceptions.EventHandler import *

class KillEventHandler(EventHandler):
  def __init__(self,
               pterm_killer: Tuple[Tuple[str,int],str,str],
               pos_killer: str,
               pterm_victim: Tuple[Tuple[str,int],str,str],
               pos_victim: str,
               weapon: str,
               is_headshot: bool):

    self.logger = logging.getLogger(__name__)
    self.pterm_killer = pterm_killer
    self.pos_killer = pos_killer
    self.pterm_victim = pterm_victim
    self.pos_victim = pos_victim
    self.weapon = weapon
    self.is_headshot = is_headshot

  def get_player_from_pterm(pterm):
      qs = self.session.query(Player).filter(Player.id == self.get_id_from_pterm(match.id, pterm))

      if qs.count() == 0:
        raise ReferenceToNonexistentPlayer

      return qs.one()


  def handle(self, match: Match):

    self.session = db.DBSession()

    killer = self.get_player_from_pterm(self.pterm_killer)
    victim = self.get_player_from_pterm(self.pterm_victim)

    self.logger.debug("Handling Kill event: {} killed by {}".format(self.pterm_victim[0][0],
                                                                    self.pterm_killer[0][0]))

    k = Kill(killPosition='{}', # FIXME
             killerPosition='{}', # FIXME 
             weaponId=None, # FIXME
             killedId=victim.id,
             killerId=killer.id,
             matchId=match.id,
             roundId=1, # FIXME
             isHeadshot=self.is_headshot,
    )

    self.session.add(k)
    self.session.commit()
