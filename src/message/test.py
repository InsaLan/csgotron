import parser as p
import lexer as l

m= l.MonLexer()
m.build()
m.test('"Claren<4><123><CT>" assisted killing "Clarence<3><BOT><TERRORIST>"'  )
m.test('"Adrian<14><BOT>" switched from team <Unassigned> to <TERRORIST>')
m.test('"Ivan<20><BOT><CT>" [-11960 4192 3584] attacked "Jeff<22><BOT><TERRORIST>" [-11282 3856 3585] with "hkp2000" (damage "19") (damage_armor "9") (health "21") (armor "70") (hitgroup "stomach")')
m.test('"Hank<21><BOT><CT>" [-11280 7479 3585] killed "Chet<18><BOT><TERRORIST>" [-11450 7628 3648] with "usp_silencer"')
m.test('eBot triggered "Round_Spawn"')
m.test('World triggered "Round_Start"')
n= p.MonParser()
n.test('"Claren<4><BOT><CT>" assisted killing "Clarence<3><BOT><TERRORIST>"')
n.test('"Ivan<20><BOT><CT>" [-11960 4192 3584] attacked "Jeff<22><BOT><TERRORIST>" [-11282 3856 3585] with "hkp2000" (damage "19") (damage_armor "9") (health "21") (armor "70") (hitgroup "stomach")')
