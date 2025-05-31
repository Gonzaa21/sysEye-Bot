from dotenv import load_dotenv
import os
import discord
import img_generator as generator
from img_generator import buf
from datetime import datetime
load_dotenv()

# permissions
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ready
@client.event
async def on_ready():
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(f'We have logged in as {client.user}')
    df, name = generator.load_last_snapshot()
    
    if df.empty:
        print("⚠️ snapshot empty")
    else:
        generator.generate_graphs(df)
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(file=discord.File(fp=buf, filename=f"dashboard_{TIMESTAMP}.png"))
    await client.close()

# dotenv
DISCORD_TOKEN = os.getenv('DISCORD-TOKEN')
CHANNEL_ID = int(os.getenv("CHANNEL-ID"))
client.run(DISCORD_TOKEN)
