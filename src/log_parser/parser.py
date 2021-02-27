import ply.yacc as yacc

from src.log_parser.lexer import LogLexer

from src.io.event_handlers.switch_team import *
from src.io.event_handlers.entered_game import *
from src.io.event_handlers.kill import *

class BadMessageException(Exception):
  pass

class LogParser(object):
    def parse(self, payload):
        res = self._parser.parse(payload)
        #print(res)
        if res:
          return res
        else:
          raise BadMessageException

    def test(self, data):
        res = self._parser.parse(data)
        print(res)

    def __init__(self, the_lexer=None):
        if the_lexer is None:
            the_lexer = LogLexer()
        self._lexer = the_lexer
        the_lexer.build()
        self.tokens = self._lexer.tokens

        self._parser = yacc.yacc(module=self)

    def p_expression_entered_game(self, p):
            'expression : pterm ENTERED'
            pterm = p[1]
            p[0] = "{}".format(pterm)
            self.out = EnteredGameEventHandler(player_name=pterm[0][0],
                                               player_uid=pterm[0][1],
                                               player_steam_id=pterm[1])

    def p_expression_switch(self,p):
            'expression : pterm SWITCH TEAM TO TEAM'
            pterm = p[1]
            p[0] = "{} {} {}".format(pterm, p[3], p[5])
            self.out = SwitchTeamEventHandler(player_uid=pterm[0][1],
                                              player_steam_id=pterm[1],
                                              src_team=p[3],
                                              dst_team=p[5])

    def p_expression_assist(self,p):
            'expression : pterm ASSIST pterm'
            p[0]= "{} {} {}".format(p[1], p[2], p[3])

    def p_expression_defuse(self,p):
            'expression : pterm TRIGGERED DEFUSEBOMB'
            p[0]= "{} {}".format(p[1], p[3])

    def p_expression_plant(self,p):
            'expression : pterm TRIGGERED PLANTBOMB'
            p[0]= "{} {}".format(p[1], p[3])

    def p_expression_attack(self,p):
            'expression : pterm POS ATTACKED pterm POS WITH WEAPON ATTACK ATTACK ATTACK ATTACK HITGROUP'
            p[0]= "{} {} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], p[12])

    def p_expression_kill(self,p):
            '''expression : pterm POS KILLED pterm POS WITH WEAPON 
                            | pterm POS KILLED pterm POS WITH WEAPON HEADSHOT'''
            if len(p)==8 :
                p[0] = "{} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], " false")
                self.out = KillEventHandler(pterm_killer = p[1],
                                            pos_killer = p[2],
                                            pterm_victim = p[4],
                                            pos_victim = p[5],
                                            weapon = p[7],
                                            is_headshot = False)


            else :
                p[0] = "{} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], " true")
  
    def p_term_steamid(self,p):
          '''playerid : STEAMIDPREFIX NUMBER ELLIPSIS NUMBER ELLIPSIS NUMBER
                        | BOT'''
          if len(p) > 2:
                steamid64 = (int(p[2]) << 56) | (1 << 52) | (1 << 32) | (int(p[6]) << 1) | int(p[4])

                p[0] = str(steamid64)

          else:
                p[0] = p[1]

    def p_term_player(self,p):
            '''pterm : NAME LOWER playerid UPPER TEAMQ
                      | NAME LOWER playerid UPPER DQUOTE'''
            if len(p[5]) > 2:
              p[0]= (p[1], p[3], p[5])
            else:
              p[0]= (p[1], p[3], None)


    def p_term_round_messages(self,p):
          '''expression : ROUND_START
                          | ROUND_END 
                          | ROUND_SPAWN'''
          p[0] = p[1]


    def p_error(self,p):
            print("Syntax error in input!", p)
            pass
    
