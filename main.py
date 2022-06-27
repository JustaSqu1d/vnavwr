from os import environ  # , getenv
from random import choice

from discord import Activity, ActivityType
from discord.ext import tasks

from api import api_run
from constants import Ships, bot, modes
from rounding import re_format

bot.activity = Activity(name="Vnav.io World Records", type=ActivityType.competing)

for ext in [
    "cogs.wr",
    "cogs.submit",
    "cogs.profile",
    "cogs.event",
    "cogs.verification",
]:
    bot.load_extension(ext)


@tasks.loop(minutes=2)
async def congrats():
    db = bot.db.find_one({"Name": "WR"})
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

    await bot.change_presence(
        activity=Activity(name=f"{person}'s {score} {ship}", type=ActivityType.watching)
    )


@bot.event
async def on_ready():
    print("Online!")
    congrats.start()


api_run()
bot.run(environ["BOTTOKEN"])
