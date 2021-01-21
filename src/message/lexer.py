import ply.lex as lex

class MonLexer(object):

    tokens = ( 
        'ATTACKED',
        'HITGROUP',
        'ATTACK',
        'DEFUSEBOMB',
        'SFUI',
        'PLANTBOMB',
        'GOTBOMB',
        'ENTERED',
        'TRIGGERED',
        'ROUND_END',
        'ROUND_START',
        'ROUND_SPAWN',
        'SAY',
        'SAYTEAM',
        'SCORED',
        'T',
        'P',
        'TO',
        'SWITCHTEAM',
        #'JOINTEAM',
        'THREW',
        'KILLED',
        'WITH',
        'LOWER',
        'UPPER',
        'POS',
        'NUMBER',
        'TEAM',
        'TEAMQ',
        'QTEAMQ',
        'WEAPON',
        'ASSIST',
        'STUFF',
        #'ID',
        'DQUOTE',
        'NAME',
        'STEAMID',
        'HEADSHOT',
        #"SPACE",

    )
    t_HEADSHOT = r'/s(headshot)'
    t_ATTACKED = r'\sattacked\s'
    t_HITGROUP = r'\s\(hitgroup\s"[a-z\s]+"\)'
    t_ATTACK = r'\s\((health|damage|damage_armor|armor)\s"[0-9]+"\)'
    t_DEFUSEBOMB = r'"Begin_Bomb_Defuse_With(out)?_Kit"'
    t_PLANTBOMB = r'"Planted_The_Bomb"'
    t_ENTERED = r'\sentered\sthe\sgame'
    t_GOTBOMB = r'"Got_The_Bomb"'
    t_SFUI = r'"SFUI_Notice_(Terrorists_Win|CTs_Win|Target_Bombed|Target_Saved|Bomb_Defused)"'
    t_TRIGGERED = r'\strigerred\s'
    t_ROUND_SPAWN = r'eBot\striggered\s"Round_Spawn"'
    t_ROUND_START = r'World\striggered\s"Round_Start"'
    t_ROUND_END = r'World\striggered\s"Round_End"'
    t_T = r'Team\s'
    t_P = r'\splayers'
    t_SCORED = r'\sscored\s'
    t_QTEAMQ = r'"(CT|TERRORIST)"'
    t_SWITCHTEAM = r'\sswitched\sfrom\steam\s'
    t_TO = r'\sto\s'
    t_STUFF = r'hegrenade|flashbang|smokegrenade|decoy|molotov'
    t_THREW = r'\sthrew\s'
    t_ASSIST = r'\sassisted\skilling\s'
    t_WEAPON = r'"[A-Za-z][a-zA-Z0-9\s_]+"'
    t_KILLED = r'\skilled\s'
    t_WITH = r'\swith\s' 
    t_TEAM = r'<(TERRORIST|CT|Unassigned|Spectator)>'
    t_TEAMQ = r'<(TERRORIST|CT|Unassigned|Spectator)>"'
    t_LOWER = r'<'
    t_UPPER = r'>'
    t_NUMBER = r'[0-9]+'
    t_POS = r'\s\[-?[0-9]+\s-?[0-9]+\s-?[0-9]+\]'
    t_DQUOTE = r'"' 
    t_NAME = r'".{2,32}<[0-9]{1,2}>'
    #t_ID = r'[0-9]+'
    t_SAYTEAM = r'\ssay_team\s".*"'
    t_SAY = r'\ssay\s".*"'

    def t_STEAMID(self,t):
         r'(BOT|STEAM_[0-9:]+)'
         return t

    #t_SPACE = r'\s'
    



    def t_error(self,t):
         print("Illegal character '%s'" % t.value[0])
         t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer= lex.lex(module=self, **kwargs)
    
    def test(self,data):
        self.lexer.input(data)
        while True:
              tok = self.lexer.token()
              if not tok: 
                  break
              print(tok)