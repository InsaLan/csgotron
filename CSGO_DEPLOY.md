# Deploy and connect to a CSGO server

1. Run the CSGO server container:

`docker run -it -p 27015:27015/tcp -p 27015:27015/udp -p 27020:27020/udp -e SRCDS_TOKEN="xxx" -v $(pwd)/csgo-dedicated:/home/steam/csgo-dedicated/ --name=csgo-dedicated cm2network/csgo`

+ This command will download CSGO in a new folder called csgo-dedicated on your current directory, you'll need ~55GB of space. The command will download csgo one time and won't download it again when you launch the container.
+ Change `SCRDS_TOKEN` to your Steam gameserver token (https://steamcommunity.com/dev/managegameservers)
+ Default server password is `changeme` and default RCON password is `changeme`.
+ If you're running the game on the same PC as the server, you may need to change the port mapped by docker on the host because 27015 may already be in use by CSGO. After that you'll need to specify the port in the connect command in step 2 `connect <server ip>:<newport>`.

2. Launch CSGO on your PC, open the console and type `connect <server local ip>; password changeme`
