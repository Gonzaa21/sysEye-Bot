from dotenv import load_dotenv
import os
import discord
load_dotenv()

# permissions
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# send message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# dotenv
DISCORD_TOKEN = os.getenv('DISCORD-TOKEN')
CHANNEL_ID = int(os.getenv("CHANNEL-ID"))
client.run(DISCORD_TOKEN)
