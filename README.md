# confinebot
**Confinebot** is InsaLan's rewrite of [eBot](https://github.com/deStrO/eBot-CSGO), a full managed server-bot for CS:GO intended to ease match creation and stats collection.

### Architecture
* confinebot (this repo) : the API backend
* confinebot-frontend : the web UI
* confinebot-spawner : an optional component that spawns CS:GO containers on specified hosts using docker.

### Technologies in use
* Language: Python 3
* API framework : aio-http
* SQL database: SQLite3 or PostgreSQL
* SQL ORM : SQLAlchemy
* RCON interface : [aiorcon](https://github.com/InsaLan/aiorcon)

### Build a development environment
1. Install python3 and pip
2. Activate `venv/bin/activate`
3. Install dependencies: `pip3 install -r requirements.txt`
4. Run the backend: `./main.py` 
