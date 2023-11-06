import discord
from discord.ext import commands
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

TOKEN = 'YOUR_BOT_TOKEN'
GUILD_ID = 1234
CHANNEL_ID = 1234

bot = commands.Bot(command_prefix='!')

# Regex pattern to match URLs
URL_REGEX = r"(https?://[^\s]+)"

# Function to save song link to Firestore
async def save_song_link(song_link):
    doc_ref = db.collection('song_links').document()
    doc_ref.set({
        'url': song_link
    })

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    print(f"Connected to {guild.name}")

@bot.event
async def on_message(message):
    # Ensure the bot does not reply to itself
    if message.author == bot.user:
        return

    # Check if the message is in the designated channel
    if message.channel.id == CHANNEL_ID:
        # Check if the message contains a URL using regex
        urls = re.findall(URL_REGEX, message.content)
        if urls:
            for url in urls:
                print(f"Song Link Detected: {url}")
                await save_song_link(url)
                await message.channel.send(f"Song link saved: {url}")

    # Process commands
    await bot.process_commands(message)

# Command to retrieve saved song links
@bot.command(name='songs', help='Displays the saved song links.')
async def on_songs_command(ctx):
    song_links = db.collection('song_links').stream()
    songs = [song_link.to_dict()['url'] for song_link in song_links]
    if songs:
        await ctx.send("\n".join(songs))
    else:
        await ctx.send("No song links have been saved yet.")

bot.run(TOKEN)
