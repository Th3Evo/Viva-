import discord
from datetime import datetime, timedelta
from Moderation.moderation import load_banned_words, banned_words
import os
import json


my_secret = os.getenv('bottoken')
TOKEN = None
if my_secret:
    TOKEN = my_secret.strip()
    
    if TOKEN.startswith("“") and TOKEN.endswith("”"):

        TOKEN = TOKEN[1:-1]
    print("Bot token successfully retrieved.")
else:
    print("Bot token not found in the environment variables!")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_banned_words()


lastPing = None

@client.event
async def on_ready():
    print(f"{client.user} is now running!")

@client.event
async def on_message(message):
    global lastPing
    if message.author == client.user:
        return

    user_message = str(message.content).lower()

    for word in banned_words:
        if word in user_message:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Please refrain from using banned words.")
            return

    if "!ping" in user_message:
        current_time = datetime.now()


        if lastPing is None or (current_time - lastPing) > timedelta(minutes=15):
            lastPing = current_time

            await message.channel.send("@here")
            await message.channel.send("Come and sign for a match")
        else:

            time_remaining = timedelta(minutes=15) - (current_time - lastPing)
            time_remaining_seconds = time_remaining.total_seconds()


            time_remaining_minutes = round(time_remaining_seconds / 60, 1)

            await message.channel.send(f"Calm down! I just used all my poor thinking power to ping you all! You need to wait {time_remaining_minutes} minutes before using !ping again.")


        await message.delete()

if TOKEN:
    client.run(TOKEN)
