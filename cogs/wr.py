from asyncio import gather
from time import time

from constants import Ships, bot, places, shipsall, re_format
from discord import ButtonStyle, Embed, Option, SlashCommandGroup, Cog
from discord.ext.pages import Page, Paginator
from discord.ui import Button, View
from discord.utils import basic_autocomplete


class Wrall(Cog):
    def __init__(self, bot):
        self.bot = bot

    wr = SlashCommandGroup(
        name="worldrecords", description="world records and their leaderboards"
    )

    @wr.command(name="all", description="Check all the top current World Records!")
    async def worldrecords(self, ctx):
        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")
        await ctx.defer()

        start_time = time()
        pages = []
        db2 = bot.db.find_one({"Name": "WR"})

        async def lb_format(ship, db2, mode, view):
            entry = db2[ship][mode]["High Score"]["1"]
            us = entry["user"].split("|")
            score = re_format(int(us[1]))
            user = await self.bot.fetch_user(us[0])
            view.add_item(
                Button(
                    style=ButtonStyle.link,
                    label=f"{user.name}-{score} ({ship})",
                    url=entry["link"],
                )
            )
            return f"\n\u001b[0;31m{user.name}-{score}\n"

        async def ships_f(embed):
            embed.insert_field_at(
                index=1,
                name="Ship",
                value="".join([f"\n**{ship}**\n" for ship in ships]),
                inline=True,
            )

        async def ffa(embed, view):
            val = "".join(
                [
                    "\n\u001b[0;31m-----\n"
                    if db2[ship]["FFA"]["High Score"]["1"]["user"] == 0
                    else await lb_format(ship, db2, "FFA", view)
                    for ship in ships
                ]
            )
            embed.insert_field_at(
                index=1, name="FFA", value=f"```ansi{val}```", inline=True
            )

        async def tdm2(embed, view):
            val = "".join(
                [
                    "\n\u001b[0;31m-----\n"
                    if db2[ship]["2 Teams"]["High Score"]["1"]["user"] == 0
                    else await lb_format(ship, db2, "2 Teams", view)
                    for ship in ships
                ]
            )
            embed.insert_field_at(
                index=2, name="2 Teams", value=f"```ansi{val}```", inline=True
            )

        for ships in shipsall:
            embed = Embed(title="Vnav.io World Records", color=ctx.guild.me.color)
            embed.set_footer(text="Created by just a squid#5483")

            view = View()
            coros = [ships_f(embed), ffa(embed, view), tdm2(embed, view)]
            await gather(*coros)

            pages.append(Page(embeds=[embed], custom_view=view))

        paginator = Paginator(
            pages=pages, loop_pages=True, timeout=120.0, disable_on_timeout=True
        )
        await paginator.respond(ctx.interaction)
        end_time = time()
        print(
            f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
        )

        return

    @wr.command(name="ship", description="Look for a specific ship's world records!")
    async def worldrecordsship(
        self,
        ctx,
        ship: Option(
            str,
            "Pick a ship! We'll handle the rest.",
            autocomplete=basic_autocomplete(Ships),
        ),
        gamemode: Option(
            str, "Choose a gamemode!", choices=["FFA", "2 Teams"], required=True
        ),
        category: Option(
            str,
            "Choose a category!",
            choices=["High Score", "Fast 500k", "Fast 1m", "Fast 1.5m"],
            required=True,
        ),
    ):
        start_time = time()

        if ship not in Ships:
            await ctx.respond("Please select a valid ship.", ephemeral=True)
            return

        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")
        await ctx.defer()

        async def lb_format(db, type_, place):
            if type_ == "players":
                try:
                    player, evidence = db["user"].split("|")[0], db["link"]
                    player2 = await self.bot.fetch_user(player)
                    return (
                        f"\n[{player2.name}]({evidence})\n"
                        if place != "Mobile 1st"
                        else f"\n**Mobile**\n\n[{player2.name}]({evidence})\n"
                    )
                except AttributeError:
                    return (
                        f"\n-----\n"
                        if place != "Mobile 1st"
                        else f"\n**Mobile**\n\n-----\n"
                    )
            elif type_ == "scores":
                try:
                    score = "{:,}".format(int(db["user"].split("|")[1]))
                    return (
                        f"\n{score}\n"
                        if place != "Mobile 1st"
                        else f"\n**Score**\n\n{score}\n"
                    )
                except AttributeError:
                    return (
                        f"\n-----\n"
                        if place != "Mobile 1st"
                        else f"\n**Mobile**\n\n-----\n"
                    )
            elif type_ == "times":
                if db["min"] + db["sec"] + db["hour"] == 0:
                    return (
                        f"\n-----\n"
                        if place != "Mobile 1st"
                        else f"\n**Mobile**\n\n-----\n"
                    )
                time_ = (
                    f"{db['min']}m {db['sec']}s"
                    if db["hour"] == 0
                    else f"{db['hour']}h {db['min']}m {db['sec']}s"
                )
                return (
                    f"\n{time_}\n"
                    if place != "Mobile 1st"
                    else f"\n**Time**\n\n{time_}\n"
                )

        async def player(embed):
            embed.insert_field_at(
                index=0,
                name="Player",
                value="".join(
                    [
                        await (
                            lb_format(
                                db2[ship][gamemode][category][place], "players", place
                            )
                        )
                        for place in places
                    ]
                ),
                inline=True,
            )

        async def score(embed):
            embed.insert_field_at(
                index=1,
                name="Score",
                value="".join(
                    [
                        await lb_format(
                            db2[ship][gamemode][category][place], "scores", place
                        )
                        for place in places
                    ]
                ),
                inline=True,
            )

        async def time_(embed):
            embed.insert_field_at(
                index=2,
                name="Time",
                value="".join(
                    [
                        await lb_format(
                            db2[ship][gamemode][category][place], "times", place
                        )
                        for place in places
                    ]
                ),
                inline=True,
            )

        db2 = bot.db.find_one({"Name": "WR"})

        embed = Embed(
            title=f"{ship} ({gamemode}) {category} Leaderboard",
            color=ctx.guild.me.color,
        )

        coros = [score(embed), time_(embed), player(embed)]
        await gather(*coros)

        embed.set_footer(text="Created by just a squid#5483")

        await ctx.followup.send(embed=embed)

        end_time = time()
        print(
            f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
        )

        return

    @wr.command(name="api", description="For developer nerds only.")
    async def api(self, ctx):
        await ctx.respond(
            embed=Embed(
                title="Vnav.io World Records API", url="https://vnavwr.up.railway.app/"
            ),
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(Wrall(bot))
