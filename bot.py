import os
import certifi
import asyncio
import discord
from discord.ext import commands
from discord import Intents
import re
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import json

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()


# Initialize Firebase
firebase_service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT")
cred = credentials.Certificate(json.loads(firebase_service_account))
firebase_admin.initialize_app(cred)

db = firestore.client()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Define Intents
intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialize Bot with Intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Regex pattern to match URLs
URL_REGEX = r"(https?://[^\s]+)"

last_saved_song_link_id = None


def save_song_link(song_link):
    global last_saved_song_link_id
    doc_ref = db.collection("song_links").document()
    try:
        doc_ref.set({"url": song_link})
        last_saved_song_link_id = doc_ref.id  # Update the last saved song link ID
        return True  # Success
    except Exception as e:
        print(f"Error saving song link: {e}")
        return False  # Error occurred


def on_save_complete(future):
    if future.exception() is not None:
        print(f"Error saving song link: {future.exception()}")
    else:
        print("Song link saved successfully")


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    print(f"Connected to {guild.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHANNEL_ID:
        urls = re.findall(URL_REGEX, message.content)
        if urls:
            for url in urls:
                print(f"Song Link Detected: {url}")
                save_song_link(url)  # Call the function without 'await'
                await message.channel.send(f"Song link saved successfully")

    await bot.process_commands(message)


@bot.command(name="delete_last", help="Deletes the last posted song link.")
async def on_delete_last_command(ctx):
    global last_saved_song_link_id
    if last_saved_song_link_id:
        try:
            db.collection("song_links").document(last_saved_song_link_id).delete()
            await ctx.send("Last song link deleted successfully.")
            last_saved_song_link_id = None
        except Exception as e:
            await ctx.send(f"Error deleting song link: {e}")
    else:
        await ctx.send("No song link available to delete.")


@bot.command(name="songs", help="Displays the saved song links.")
async def on_songs_command(ctx):
    song_links = db.collection("song_links").stream()
    songs = [song_link.to_dict()["url"] for song_link in song_links]
    if songs:
        await ctx.send("\n".join(songs))
    else:
        await ctx.send("No song links have been saved yet.")


bot.run(TOKEN)
