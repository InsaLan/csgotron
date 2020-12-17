import parser as p

m= p.MonLexer()
m.build()
m.test("<12[1 45 78]><CT>")