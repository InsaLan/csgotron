
curl -s --request POST \
  --url http://localhost:8080/team \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "a",
	"nationality": "France"
}' > /dev/null

curl -s --request POST \
  --url http://localhost:8080/team \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "b",
	"nationality": "France"
}' > /dev/null

curl -s --request POST \
  --url http://localhost:8080/server \
  --header 'Content-Type: application/json' \
  --data '{
	"ip": "10.0.0.157",
	"port": 27015,
	"nickname": "cs1"
}' > /dev/null

curl -s --request POST \
  --url http://localhost:8080/match \
  --header 'Content-Type: application/json' \
  --data '{
	"idTeamA": 1,
	"idTeamB": 2,
	"idServer": 1,
	"map": "de_dust",
	"maxRound": 32,
	"password": "changeme"
}' > /dev/null

