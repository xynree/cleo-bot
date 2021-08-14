import discord
import random
import os
from dotenv import load_dotenv

client = discord.Client()

load_dotenv()

meow_list = ["mrowW", "mow!", "mewww", "mrew!", "MROWWW", "brrr", "mohwr", "meeeOW", "mrrrrrr", "MeOW", "meeewwwee!"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$cleo'):
        await message.channel.send(random.choice(meow_list))

TOKEN = os.getenv("TOKEN");
client.run(TOKEN)