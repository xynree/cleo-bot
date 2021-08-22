import discord
from discord.ext import tasks, commands
import random
import os
import time
from dotenv import load_dotenv
from threading import Event, Thread
import requests

client = discord.Client()
load_dotenv()

meow_list = ["mrowW", "mow!", "mewww", "mrew!", "MROWWW", "brrr", "mohwr", "meeeOW",
             "mrrrrrr", "MeOW", "meeewwwee!", "meeeeOwoOo", "meow", "mow mow", "meo meo mew!"]
meow = random.choice(meow_list)


outside = False
fed = False
pet_count = 0
secs = 30

# On ready/Start Up events


@tasks.loop(seconds=secs)
async def constantMeow():
    gardenzone = client.get_channel(735622629469323396)
    await gardenzone.send(random.choice(meow_list))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    gardenzone = client.get_channel(735622629469323396)
    await gardenzone.send('>>> Cleo is here!')

    if not constantMeow.is_running():
        constantMeow.start()


# On Message Send

@client.event
async def on_message(message):

    global fed
    global secs
    global outside
    global pet_count
    global meow

    msg = message.content
    send = message.channel.send
    user = message.author

    if message.author == client.user:
        return

# Cleo Outside

    if msg == '$cleooutside':
        if outside:
            await send('>>> Cleo is already outside!')
        else:
            outside = True
            constantMeow.cancel()
            await send(' >>> You put Cleo outside!')

# Cleo Meow

    if msg == '$cleo':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else:
            await send(meow)
    if msg == '$fact':

        r = requests.get(url="https://catfact.ninja/fact?max_length=140")
        fact = r.json()
        await send(f">>> {fact.get('fact')}")
# Find Cleo
    if msg == '$findcleo':
        if not(outside):
            await send(meow)
        else:
            randomint = random.randint(0, 9)
            if randomint > 5:
                outside = False
                constantMeow.start()
                await send('>>> You put Cleo back inside!')
                await send(meow)
            else:
                await send('>>> You could not find Cleo. Try again later!')
# Pet Cleo
    if msg == '$pet':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else:
            secs = secs + 10
            constantMeow.change_interval(seconds=secs)

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
# Feed cleo
    if msg == '$feed':
        if outside:
            await send('>>> Cleo is outside! Type $findcleo to search!')
        else:
            secs = secs + 20
            constantMeow.change_interval(seconds=secs)

            fed = True
            await send('>>> Cleo has been fed! She slurps up her food happily.')
# Cleo Shut up
    if msg == '$shutup':
        constantMeow.cancel()
        await send('>>> Cleo zipped it.')
# Cleo Help Command
    if msg == '$help':
        emb = discord.Embed(title='Cleo Bot Commands')
        emb.add_field(name='$cleo', value='Say hi to Cleo!', inline=False)
        emb.add_field(
            name='$shutup', value='Cleo is being too loud. Tell her to stop.', inline=False)
        emb.add_field(name='$cleooutside',
                      value='Put Cleo outside.', inline=False)
        emb.add_field(
            name='$findcleo', value='Only works if Cleo is outside. Look for Cleo outside.', inline=False)
        emb.add_field(
            name='$pet', value='Give Cleo a pet!', inline=False)
        emb.add_field(
            name='$feed', value='Feed Cleo.', inline=False)
        emb.add_field(
            name='$fact', value='Ask for a cat fact.', inline=False)
        emb.add_field(
            name='$roles', value='Display List of roles', inline=False)
        await send(embed=emb)

# Cleo List Roles
    if msg == '$roles':
        emb = discord.Embed(title='Roles')
        emb.add_field(name='Baby', value='$rolebaby', inline=False)
        emb.add_field(
            name='Busby', value='$rolebusby', inline=False)
        await send(embed=emb)

# Cleo Role Change

    if msg == '$rolebaby':
        baby = discord.utils.get(message.guild.roles, name='baby')
        await user.add_roles(baby)
        await send(f">>> {user} was assigned to role 'baby'!")

    if msg == '$rolebusby':
        busby = discord.utils.get(message.guild.roles, name='busby')
        await user.add_roles(busby)
        await send(f">>> {user} was assigned to role 'busby'!")


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
