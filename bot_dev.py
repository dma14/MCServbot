import os
import discord
import signal
import sys
import asyncio
from dotenv import load_dotenv
from mcstatus import MinecraftServer

# Grab environment variables for discord server
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_TOKEN')
channel_name = os.getenv('NOTIF_CHANNEL_NAME')

# Grab minecraft server data as well
mcserv_info = os.getenv('SERVER_ADDRESS')

# Initialize discord client
client = discord.Client()

# initialize mcserv model
mcserv = MinecraftServer.lookup(mcserv_info)

# Catch sigint for when we close this program
exit_condition = False
def signal_handler(sig, frame):
    printf('SIGINT detected, closing...')
    exit_condition = True

signal.signal(signal.SIGINT, signal_handler)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    for mcserv_text_channel in guild.text_channels:
        if mcserv_text_channel.name.partition('-')[0] == channel_name:
            break

    for role in guild.roles:
        if role.name == "Minecraft":
            break

    server_status = False
    current_player_count = 0

    while not exit_condition:
        try:
            # Check server status
            status = mcserv.status()
            # print("The server has {0} players and replied in {1} ms.".format(status.players.online, status.latency))
            if not server_status:
                announcement_msg = await mcserv_text_channel.send("{0} Server\'s up!".format(role.mention))
                await mcserv_text_channel.edit(name="mcserv-online")
                server_status = True

            if server_status:
                if current_player_count != status.players.online:
                    await announcement_msg.edit(content="{0} Server's up! Current player count: {1}".format(role.mention, status.players.online))
        except Exception as e:
            # Case when server is down
            print(e)
            # print("The server is down!")
            await mcserv_text_channel.edit(name="mcserv-offline")
            # await mcserv_voice_channel.edit(name="server offline")

        # Pause for a bit so we're not constantly pinging
        # Rate limit for channel names as of 29/5/2020 is 2 changes per 10 minutes
        await asyncio.sleep(10)
    # Exit condition reached, close out now
    print('Exiting!')

try:
    client.run(TOKEN)
except KeyboardException as e:
    print(e)
