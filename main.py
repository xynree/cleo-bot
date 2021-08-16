import discord
import random
import os
from dotenv import load_dotenv

client = discord.Client()

load_dotenv()

meow_list = ["mrowW", "mow!", "mewww", "mrew!", "MROWWW", "brrr", "mohwr", "meeeOW", "mrrrrrr", "MeOW", "meeewwwee!", "meeeeOwoOo", "meow", "mow mow", "meo meo mew!"]

outside = False
fed = False
pet_count = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global fed
    global outside
    global pet_count
    meow = random.choice(meow_list)
    msg = message.content
    send = message.channel.send

    if message.author == client.user:
        return

    if msg == '$cleooutside':
        if outside:
            await send('>>> Cleo is already outside!')
        else:
            outside = True
            await send(' >>> You put Cleo outside!')
    if msg == '$cleo':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else:
            await send(meow)
    if msg == '$findcleo':
        if not(outside):
            await send(meow)
        else:
            randomint = random.randint(0,9)
            if randomint > 5:
                outside = False
                await send('>>> You put Cleo back inside!')
                await send(meow)
            else:
                await send('>>> You could not find Cleo. Try again later!')
    if msg == '$pet':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else:
            pet_count = pet_count + 1
            if pet_count < 4:
                if pet_count == 1:
                    await send('>>> Cleo headbutts you happily.')
                    await send(meow)
                if pet_count == 2:
                    await send('>>> Cleo sticks her butt up in the air.')
                    await send(meow)
                if pet_count == 3:
                     await send('>>> Cleo wiggles under your hand.')
                     await send(meow)
            else:
                await send('>>> Cleo gives you a little nip! Try again later.')
                pet_count = 0
    if msg == '$feed':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else: 
            fed = True
            await send('>>> Cleo has been fed! She slurps up her food happily.')
            await send(meow)
    

TOKEN = os.getenv("TOKEN");
client.run(TOKEN)