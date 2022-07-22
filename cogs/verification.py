from datetime import datetime
from time import time

from bson import encode
from bson.raw_bson import RawBSONDocument
from constants import DenialReason, bot, places_mobile, placesPC
from discord import Color, Embed, message_command, Cog


class Verification(Cog):
    def __init__(self, bot):
        super().__init__()

    @message_command(name="deny", guild_ids=[588921569271611393])
    async def deny(self, ctx, msg):
        if ctx.channel.id != 915211422475108393:
            return

        modal = DenialReason(msg, ctx)
        await ctx.interaction.response.send_modal(modal)

    @message_command(name="approve", guild_ids=[588921569271611393])
    async def approve(self, ctx, msg):
        start_time = time()

        if ctx.channel.id != 915211422475108393:
            return

        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")

        await ctx.defer(ephemeral=True)

        submissions = bot.db.find_one({"_id": "submissions"})

        if str(msg.id) not in submissions:
            await ctx.followup.send("No submission found.")
            end_time = time()
            print(
                f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
            )
            return

        submission = submissions[str(msg.id)]
        author_id = submission["author_id"]

        ship, seconds, minutes, hours, evidence, score, platform, gamemode = (
            submission["ship"],
            submission["sec"],
            submission["min"],
            submission["hour"],
            submission["link"],
            submission["score"],
            submission["platform"],
            submission["gamemode"],
        )
        IGtimesec = (seconds) + (minutes * 60) + (hours * 3600)

        mobile = False if platform == "PC" else True

        arry = {
            author_id: {
                "author_id": author_id,
                "score": score,
                "evidence": evidence,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
                "mobile": mobile,
                "ship": ship,
                "mode": gamemode,
                "hour": hours,
                "minute": minutes,
                "second": seconds,
                "link": evidence,
                "user": author_id,
            }
        }

        bot.db.update_one(
            {"_id": "personal best"},
            {
                "$set": RawBSONDocument(
                    encode(
                        {f"{author_id} | {score} {ship} {gamemode}": arry[author_id]}
                    )
                )
            },
        )

        categories = ["High Score"]

        if score >= 500000:
            categories.append("Fast 500k")
        if score >= 1000000:
            categories.append("Fast 1m")
        if score >= 1500000:
            categories.append("Fast 1,5m")

        db = bot.db.find_one({"Name": "WR"})

        for author in arry.copy():
            for category in categories:
                IGtimesec = (
                    (arry[author]["seconds"])
                    + (arry[author]["minutes"] * 60)
                    + (arry[author]["hours"] * 3600)
                )

                if arry[author]["mobile"]:
                    for place in places_mobile:
                        if db[ship][gamemode][category][place]["user"] == 0:
                            bot.db.update_one(
                                {"Name": "WR"},
                                {
                                    "$set": {
                                        f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                            encode(
                                                {
                                                    "user": f"{author_id}|{score}",
                                                    "link": evidence,
                                                    "hour": hours,
                                                    "min": minutes,
                                                    "sec": seconds,
                                                }
                                            )
                                        )
                                    }
                                },
                            )

                            break

                        elif "Fast" in category:
                            time_ = (
                                (db[ship][gamemode][category][place]["sec"])
                                + (db[ship][gamemode][category][place]["min"] * 60)
                                + (db[ship][gamemode][category][place]["hour"] * 3600)
                            )
                            if IGtimesec < time_:
                                author_score = db[ship][gamemode][category][place][
                                    "user"
                                ]
                                author_id2 = author_score.split("|")[0]
                                score2 = author_score.split("|")[1]

                                evidence2 = db[ship][gamemode][category][place]["link"]
                                hours2 = db[ship][gamemode][category][place]["hour"]
                                minutes2 = db[ship][gamemode][category][place]["min"]
                                seconds2 = db[ship][gamemode][category][place]["sec"]

                                arry.update(
                                    {
                                        author_id2: {
                                            "author_id": author_id2,
                                            "score": score2,
                                            "evidence": evidence2,
                                            "hours": hours2,
                                            "minutes": minutes2,
                                            "seconds": seconds2,
                                            "mobile": True,
                                        }
                                    }
                                )
                                IGtimesec = (
                                    (seconds2) + (minutes2 * 60) + (hours2 * 3600)
                                )

                                bot.db.update_one(
                                    {"Name": "WR"},
                                    {
                                        "$set": {
                                            f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                                encode(
                                                    {
                                                        "user": f'{arry[author]["author_id"]}|{arry[author]["score"]}',
                                                        "link": arry[author][
                                                            "evidence"
                                                        ],
                                                        "hour": arry[author]["hours"],
                                                        "min": arry[author]["minutes"],
                                                        "sec": arry[author]["seconds"],
                                                    }
                                                )
                                            )
                                        }
                                    },
                                )

                                break

                        else:
                            author_score = db[ship][gamemode][category][place]["user"]
                            score2 = int(author_score.split("|")[1])
                            if score > score2:
                                author_score = db[ship][gamemode][category][place][
                                    "user"
                                ]
                                author_id2 = author_score.split("|")[0]
                                score2 = author_score.split("|")[1]

                                evidence2 = db[ship][gamemode][category][place]["link"]
                                hours2 = db[ship][gamemode][category][place]["hour"]
                                minutes2 = db[ship][gamemode][category][place]["min"]
                                seconds2 = db[ship][gamemode][category][place]["sec"]

                                arry.update(
                                    {
                                        author_id2: {
                                            "author_id": author_id2,
                                            "score": score2,
                                            "evidence": evidence2,
                                            "hours": hours2,
                                            "minutes": minutes2,
                                            "seconds": seconds2,
                                            "mobile": True,
                                        }
                                    }
                                )

                                bot.db.update_one(
                                    {"Name": "WR"},
                                    {
                                        "$set": {
                                            f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                                encode(
                                                    {
                                                        "user": f'{arry[author]["author_id"]}|{arry[author]["score"]}',
                                                        "link": arry[author][
                                                            "evidence"
                                                        ],
                                                        "hour": arry[author]["hours"],
                                                        "min": arry[author]["minutes"],
                                                        "sec": arry[author]["seconds"],
                                                    }
                                                )
                                            )
                                        }
                                    },
                                )
                                break

                for place in placesPC:  # not mobile / is mobile
                    print(place)
                    if db[ship][gamemode][category][place]["user"] == 0:
                        bot.db.update_one(
                            {"Name": "WR"},
                            {
                                "$set": {
                                    f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                        encode(
                                            {
                                                "user": f"{author_id}|{score}",
                                                "link": evidence,
                                                "hour": hours,
                                                "min": minutes,
                                                "sec": seconds,
                                            }
                                        )
                                    )
                                }
                            },
                        )
                        break

                    elif "Fast" in category:
                        time_ = (
                            (db[ship][gamemode][category][place]["sec"])
                            + (db[ship][gamemode][category][place]["min"] * 60)
                            + (db[ship][gamemode][category][place]["hour"] * 3600)
                        )
                        if IGtimesec < time_:
                            author_score = db[ship][gamemode][category][place]["user"]
                            author_id2 = author_score.split("|")[0]
                            score2 = author_score.split("|")[1]

                            evidence2 = db[ship][gamemode][category][place]["link"]
                            hours2 = db[ship][gamemode][category][place]["hour"]
                            minutes2 = db[ship][gamemode][category][place]["min"]
                            seconds2 = db[ship][gamemode][category][place]["sec"]

                            arry.update(
                                {
                                    author_id2: {
                                        "author_id": author_id2,
                                        "score": score2,
                                        "evidence": evidence2,
                                        "hours": hours2,
                                        "minutes": minutes2,
                                        "seconds": seconds2,
                                        "mobile": False,
                                    }
                                }
                            )
                            IGtimesec = (seconds2) + (minutes2 * 60) + (hours2 * 3600)

                            bot.db.update_one(
                                {"Name": "WR"},
                                {
                                    "$set": {
                                        f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                            encode(
                                                {
                                                    "user": f'{arry[author]["author_id"]}|{arry[author]["score"]}',
                                                    "link": arry[author]["evidence"],
                                                    "hour": arry[author]["hours"],
                                                    "min": arry[author]["minutes"],
                                                    "sec": arry[author]["seconds"],
                                                }
                                            )
                                        )
                                    }
                                },
                            )
                            break

                    else:
                        author_score = db[ship][gamemode][category][place]["user"]
                        score2 = int(author_score.split("|")[1])
                        if score > score2:
                            author_score = db[ship][gamemode][category][place]["user"]
                            author_id2 = author_score.split("|")[0]
                            score2 = author_score.split("|")[1]

                            evidence2 = db[ship][gamemode][category][place]["link"]
                            hours2 = db[ship][gamemode][category][place]["hour"]
                            minutes2 = db[ship][gamemode][category][place]["min"]
                            seconds2 = db[ship][gamemode][category][place]["sec"]

                            arry.update(
                                {
                                    author_id2: {
                                        "author_id": author_id2,
                                        "score": score2,
                                        "evidence": evidence2,
                                        "hours": hours2,
                                        "minutes": minutes2,
                                        "seconds": seconds2,
                                        "mobile": False,
                                    }
                                }
                            )

                            bot.db.update_one(
                                {"Name": "WR"},
                                {
                                    "$set": {
                                        f"{ship}.{gamemode}.{category}.{place}": RawBSONDocument(
                                            encode(
                                                {
                                                    "user": f'{arry[author]["author_id"]}|{arry[author]["score"]}',
                                                    "link": arry[author]["evidence"],
                                                    "hour": arry[author]["hours"],
                                                    "min": arry[author]["minutes"],
                                                    "sec": arry[author]["seconds"],
                                                }
                                            )
                                        )
                                    }
                                },
                            )
                            break

        embed = msg.embeds[0]
        embed.color = Color.green()
        embed.timestamp = datetime.now()
        embed.set_footer(text="Approved at")

        role_id = 929206223037952050
        ping = ctx.guild.get_role(role_id)

        await ctx.followup.send("Approved!")
        await ctx.send(f"{ping.mention} New World Record Approved!")
        await msg.edit(embed=embed)

        embed2 = Embed(
            title="Your submission has been approved!",
            url=msg.jump_url,
            color=Color.green(),
        )
        author = await bot.fetch_user(author_id)
        try:
            await author.send(embed=embed2)
        except:
            pass

        end_time = time()
        print(
            f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
        )

        return


def setup(bot):
    bot.add_cog(Verification(bot))
