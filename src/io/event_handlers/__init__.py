from src.db import models as db
from sqlalchemy import func
from src.db.models.Round import Round

class EventHandler:

  def __init__(self):
    self.session = db.DBSession()

  def get_id_from_pterm(self, match_id, pterm):
    if pterm[1] == 'BOT':                          
      return match_id * 1000 + pterm[0][1]
    return int(pterm[1])


  """
  This method retrieves the current round id for the given match
  The major assumption made here is that the current round for this is the latest round (max round id)
  associated to given match id. 
  This could fail in these cases :
    * No Round exist for the given match, in which case, this function returns None
    * If a kill is made and just after that a new round starts, there could be a race here 
      if RoundStartEventHandler is too fast, this needs to be tested later (TODO)
  """
  def get_current_round_id(self, match_id: int) -> int:
      qs = self.session.query(func.max(Round.id)).filter(Round.matchId == match_id)
      return qs.scalar()
