from discord import Activity, ActivityType
from discord.ext import tasks
from os import environ, system #, getenv
from replit import db
from rounding import re_format
from random import choice
from constants import bot, Ships, modes
from multiprocessing import Process

bot.activity = (
    Activity(
        name="Vnav.io World Records",
        type=ActivityType.competing
    )
)

for ext in [
    'cogs.wr',
	'cogs.submit', 
	'cogs.profile', 
	'cogs.event', 
	'cogs.verification'
]:
    bot.load_extension(ext)

@tasks.loop(minutes=2)
async def congrats():
    while True:
        ship = choice(Ships)
        mode = choice(modes)
        if db[ship][mode]["High Score"]["1"]["user"] != 0:
            union_author_score = db[ship][mode]["High Score"]["1"]["user"].split("|")
            person = union_author_score[0]
            score = re_format(int(union_author_score[1]))
            person = await bot.fetch_user(person)
            person = person.name
            break

    await bot.change_presence(activity = Activity(
        name=f"{person}'s {score} {ship}",
        type=ActivityType.watching
        )
    )

@bot.event
async def on_ready():
    #print(getenv("REPLIT_DB_URL")
    print("Online!")
    congrats.start()

api = Process(target=system, args=("uvicorn keepalive:app",))
api.start()
api.join()
bot.run(environ['BOTTOKEN'], reconnect = True)