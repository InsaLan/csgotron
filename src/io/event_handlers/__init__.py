class EventHandler:
  def get_id_from_pterm(self, match_id, pterm):
    if pterm[1] == 'BOT':                          
      return match_id * 1000 + pterm[0][1]
    return int(pterm[1])
