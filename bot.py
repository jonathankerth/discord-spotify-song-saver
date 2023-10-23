import discord
from discord.ext import commands

TOKEN = 'YOUR_BOT_TOKEN'
GUILD_ID = YOUR_GUILD_ID  # Replace with your server's ID
CHANNEL_ID = YOUR_CHANNEL_ID  # Replace with the channel ID where songs are posted

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    print(f"Connected to {guild.name}")

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID:
        # Simple regex to match URLs
        if 'https://' in message.content or 'http://' in message.content:
            print(f"Song Link Detected: {message.content}")

bot.run(TOKEN)
