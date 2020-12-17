import ply.lex as lex

class MonLexer(object):

    tokens = ( 
        'KILLED',
        'WITH',
        'LOWER',
        'UPPER',
        'POS',
        'NUMBER',
        'TEAM',
        'TEAMQ',
        'WEAPON',
        'ASSIST',
        'NAME',
        'STEAMID',
        #'ID',
        'DQUOTE',

    )

    t_ASSIST = r'\sassisted\skilling\s'
    t_WEAPON = r'"[A-Z][a-zA-Z0-9\s]+"'
    t_KILLED = r'\skilled\s'
    t_WITH = r'\swith\s' 
    t_TEAM = r'<(TERRORIST|CT|Unassigned|Spectator)>'
    t_TEAMQ = r'<(TERRORIST|CT|Unassigned|Spectator)>"'
    t_LOWER = r'<'
    t_UPPER = r'>'
    t_NUMBER = r'[0-9]+'
    t_POS = r'\[-?[0-9]+\s-?[0-9]+\s-?[0-9]+\]'
    t_NAME = r'".{2,32}<[0-9]>'
    #t_ID = r'[0-9]+'
    t_STEAMID = r'[^<>]+'
    t_DQUOTE = r'"' 



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