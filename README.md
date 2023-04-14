# MCServbot

A simple Discord bot that queries a MineCraft server and displays info about it in a given Discord channel. 
Requires the following environment variables to be set:

* DISCORD_TOKEN=\<Generated Discord token for the bot to use>
* DISCORD_GUILD=\<String name of the Discord server to connect to>
* NOTIF_CHANNEL_NAME=\<Channel name on the given discord server to post updates to>
* SERVER_ADDRESS=\<IP address of the MineCraft server to query>

# Features
* Posts messages when the server goes up or down.
* Posts messages showing the player count on the server.
* Polls the server every ~10 minutes (configurable)
