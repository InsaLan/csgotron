#!/bin/bash

docker run -dit -p 27015:27015/tcp -p 27015:27015/udp -p 27020:27020/udp -e SRCDS_TOKEN="$TOKENCS" -v $HOME/csgo-dedicated:/home/steam/csgo-dedicated/ --name=csgo-dedicated cm2network/csgo
rm confinebot.db

bash -c "sleep 2; ./setup.sh" & disown

python3 main.py

echo "stopping"

docker stop $(docker ps -qa) && docker rm $(docker ps -qa)
