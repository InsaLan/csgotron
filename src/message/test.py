import parser as p

m= p.MonLexer()
m.build()
m.test('"Clarence<4><BOT><CT>" assisted killing "Clarence<3><BOT><TERRORIST>"')