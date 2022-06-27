from discord import Activity, ActivityType
from discord.ext import tasks
from os import environ  # , getenv
from api import api_run
from rounding import re_format
from random import choice
from constants import bot, Ships, modes

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
    from constants import categories, places
    db = bot.db.find_one({"Name": "WR"})
    for ship in Ships:
        for mode in modes:
            for category in categories:
                for place in places:
                    entry = db[ship][mode][category][place]
                    if entry["user"] != 0:
                        user = entry["user"].split("|")[0]
                        score = entry["user"].split("|")[1]
                        link = entry["link"]
                        hour = entry["hour"]
                        minute = entry["min"]
                        second = entry["sec"]

                        entry = {
                            "user": user,
                            "score": score,
                            "link": link,
                            "hour": hour,
                            "minute": minute,
                            "second": second,
                            "ship" : ship,
                            "mode" : mode,
                        }

                        entry_name = f"{user} | {score} {ship} {mode}"

                        bot.db.update_one(
                            {"_id":"personal best"}, {"$set": {entry_name: entry}}
                        )
api_run()
bot.run(environ["BOTTOKEN"])
