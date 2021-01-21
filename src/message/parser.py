import ply.yacc as yacc
from lexer import  MonLexer

class MonParser(object):
    def test(self, data):
        res = self._parser.parse(data)
        print(res)

    def __init__(self, the_lexer=None):
        if the_lexer is None:
            the_lexer = MonLexer()
        self._lexer = the_lexer
        self.tokens = self._lexer.tokens

        self._parser = yacc.yacc(module=self)
    def p_expression_assist(self,p):
            'expression : pterm ASSIST pterm'
            p[0]= p[1] + p[2] + p[3] 

    def p_expression_defuse(self,p):
            'expression : pterm TRIGGERED DEFUSEBOMB'
            p[0]= p[1] + p[3]

    def p_expression_plant(self,p):
            'expression : pterm TRIGGERED PLANTBOMB'
            p[0]= p[1] + p[3]

    def p_expression_attack(self,p):
            'expression : pterm POS ATTACKED pterm POS WITH WEAPON ATTACK ATTACK ATTACK ATTACK HITGROUP'
            p[0]= p[1] + p[2] + p[3]+p[4]+p[5]+p[7]+p[12]

    def p_expression_kill(self,p):
            '''expression : pterm POS KILLED pterm POS WITH WEAPON 
                            | pterm POS KILLED pterm POS WITH WEAPON HEADSHOT'''
            if len(p)==8 :
                p[0]= p[1] + p[2] + p[3]+p[4]+p[5]+p[7]+" false"
            else :
                p[0]= p[1] + p[2] + p[3]+p[4]+p[5]+p[7]+" true"


    def p_term_player(self,p):
            'pterm : NAME LOWER STEAMID UPPER TEAMQ'
            p[0]= p[1] +p[2]+p[3]+p[4]+p[5]

  

    #def p_term_steam_id(self,p):
     #   'tSTEAM_ID : STEAM_ID'
      #  p[0]= p[1]
         
           

    def p_error(self,p):
            print("Syntax error in input!")
    
        
    