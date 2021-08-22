import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from discord import Intents
import random
import os
from dotenv import load_dotenv
import requests

intents = Intents.all()
bot = Bot(intents=intents, command_prefix='.')
load_dotenv()

# --- Global Constants ---
meow_list = ["mrowW", "mow!", "mewww", "mrew!", "MROWWW", "brrr", "mohwr", "meeeOW",
             "mrrrrrr", "MeOW", "meeewwwee!", "meeeeOwoOo", "meow", "mow mow", "meo meo mew!"]
meow = random.choice(meow_list)
outside = False
fed = False
pet_count = 0
secs = 30


async def outsideResponse(context):
    await context.send(f'>>> Cleo is outside! Use {bot.command_prefix}findCleo to search!')


@tasks.loop(seconds=secs)
async def constantMeow():
    gardenzone = bot.get_channel(735622629469323396)
    await gardenzone.send(random.choice(meow_list))

# --- Initialization ---


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='baby and busby'))

    if not constantMeow.is_running():
        constantMeow.start()

# --- Cleo Commands ---


@bot.command(name="cleo", help="Interact with Cleo!")
async def cleo(context):
    global outside
    if outside:
        await outsideResponse(context)
    else:
        await context.send(meow)


@bot.command(name="outside", help="Put Cleo outside!")
async def cleoOutside(context):
    global outside
    if outside:
        await outsideResponse(context)
    else:
        outside = True
        constantMeow.cancel()
        await context.send('>>> You put Cleo outside!')


@bot.command(name="findCleo", help="Search for Cleo!")
async def findCleo(context):
    global outside
    if outside:
        await outsideResponse(context)
    else:
        randomint = random.randint(0, 9)
        if randomint > 5:
            outside = False
            constantMeow.start()
            await context.send('>>> You put Cleo back inside!')
            await context.send(meow)
        else:
            await context.send('>>> You could not find Cleo. Try again later!')


@bot.command(name="pet", help="Give Cleo some love!")
async def pet(context):
    global outside
    global secs
    global pet_count
    if outside:
        await outsideResponse(context)
    else:
        secs = secs + 10
        constantMeow.change_interval(seconds=secs)
        pet_count = pet_count + 1
        if pet_count < 4:
            if pet_count == 1:
                await context.send('>>> Cleo headbutts you happily.')
                await context.send(meow)
            if pet_count == 2:
                await context.send('>>> Cleo sticks her butt up in the air.')
                await context.send(meow)
            if pet_count == 3:
                await context.send('>>> Cleo wiggles under your hand.')
                await context.send(meow)
        else:
            await context.send('>>> Cleo gives you a little nip! Try again later.')
            pet_count = 0


@bot.command(name="feed", help="Give Cleo some munch!")
async def feed(context):
    global outside
    global secs
    global fed
    if outside:
        await outsideResponse(context)
    else:
        secs = secs + 20
        constantMeow.change_interval(seconds=secs)
        fed = True
        await context.send('>>> Cleo has been fed! She slurps up her food happily.')


@bot.command(name="shutup", help="Stop that yappin!")
async def shutup(context):
    constantMeow.cancel()
    await context.send('>>> Cleo zipped it.')


@bot.command(name="fact", help="Wanna hear a fact?")
async def fact(context):
    global outside
    if outside:
        await outsideResponse(context)
    else:
        r = requests.get(url="https://catfact.ninja/fact?max_length=140")
        fact = r.json()
        await context.send(f">>> {fact.get('fact')}")


@bot.command(name="roles")
async def roles(context, *args):
    user = context.author

    if len(args) == 0:
        emb = discord.Embed(title='Roles')
        emb.add_field(
            name='Baby', value=f'{bot.command_prefix}roles baby', inline=False)
        emb.add_field(
            name='Busby', value=f'{bot.command_prefix}roles busby', inline=False)
        await context.send(embed=emb)

    if args[0] == 'baby':
        baby = discord.utils.get(context.guild.roles, name='baby')
        await user.add_roles(baby)
        await context.send(f">>> {user} was assigned to role 'baby'!")
    elif args[0] == 'busby':
        busby = discord.utils.get(context.guild.roles, name='busby')
        await user.add_roles(busby)
        await context.send(f">>> {user} was assigned to role 'busby'!")
    else:
        await context.send(f">>> {args[0]} role doesn't exist!")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
