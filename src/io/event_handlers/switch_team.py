import logging

from . import EventHandler
from src.db import models as db
from src.db.models.Match import Match
from src.db.models.Player import Player
from src.exceptions.EventHandler import *

class SwitchTeamEventHandler(EventHandler):
  def __init__(self,
               player_uid: int,
               player_steam_id: str,
               src_team: str,
               dst_team: str):
    EventHandler.__init__(self)
    self.player_uid = player_uid
    self.player_steam_id = player_steam_id

    self.src_team = src_team
    self.dst_team = dst_team

    self.logger = logging.getLogger(__name__)

  def handle(self, match: Match):
    # the SwitchTeamEvent allows us to link the Player to a Team object according to the chosen team : CT or T

    self.logger.debug("Handling SwitchTeamEvent for player id = {}".format(self.player_steam_id))
    
    # XXX: For the moment we take care of the initial team switch only and
    # we do not consider players that Spectate ('Spectator' team)

    # We decided that if the player changes team because for example
    # he made a mistake during initial assignation, it will require a 
    # manual action from tournament admin to change it in the confinebot

    if self.src_team == 'Unassigned':
      
      if self.player_steam_id == 'BOT': 
        self.player_steam_id = match.id * 1000 + self.player_uid

      qs = self.session.query(Player).filter(Player.id == self.player_steam_id)

      if qs.count() == 0:
        # XXX: this can happen if the EnteredGameEvent was not yet handled or if it was not received by log handler. 
        # Although the first part seem unlikely to happen, the second can happen in practice as the log protocol is over UDP !

        self.logger.error("SwitchTeamEvent with non existant player id = {}".format(self.player_steam_id))
        raise ReferenceToNonexistentPlayer

      player = qs.one()

      if self.dst_team == 'TERRORIST':
        player.idTeam = match.teamFirstSideT.id
      elif dst_team == 'CT':
        player.idTeam = match.teamFirstSideCT.id

      self.session.commit()
