import time
import discord
from constants import bot, re_format
from discord import Cog, user_command


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = time

    @user_command(
        name="Profile", guild_ids=[588921569271611393], default_permission=True
    )
    async def profile(self, ctx, member) -> None:
        achievements = ""

        temp = {}
        stats = discord.Embed(title="Personal Best", color=ctx.guild.me.color)

        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")
        start_time = self.time.time()

        await ctx.defer(ephemeral=True)

        all_entries = bot.db.find_one({"_id": "personal best"})

        entries = []

        for key in all_entries.keys():
            if str(member.id) in key:
                entries.append(key)

        if entries == []:
            achievements = "None. Use `/submit` to submit a run."

            stats.description = achievements
            stats.set_author(name=member.name)

            await ctx.followup.send(embed=stats)
            end_time = self.time.time()
            print(
                f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
            )
            return

        personal_bests = {}

        for entry in entries:
            personal_bests[entry] = all_entries[entry]

        print(personal_bests)
        for score in personal_bests:

            ship, mode, link, score1 = (
                personal_bests[score]["ship"],
                personal_bests[score]["mode"],
                personal_bests[score]["link"],
                int(personal_bests[score]["score"]),
            )
            if personal_bests[score]["hour"] == 0:

                sec = (
                    f'0{personal_bests[score]["second"]}'
                    if len(str(personal_bests[score]["second"])) == 1
                    else f'{personal_bests[score]["second"]}'
                )

                time = f"{personal_bests[score]['minute']}:{sec}"
            else:

                sec = (
                    f'0{personal_bests[score]["second"]}'
                    if len(str(personal_bests[score]["second"])) == 1
                    else f'{personal_bests[score]["second"]}'
                )

                min = (
                    f'0{personal_bests[score]["minute"]}'
                    if len(str(personal_bests[score]["minute"])) == 1
                    else f'{personal_bests[score]["minute"]}'
                )

                time = f"{personal_bests[score]['hour']}:{min}:{sec}"

            if not (f"[{ship} {time} ({mode})]" in temp):

                temp[f"[{ship} {time} ({mode})]({link})\n"] = score1

        templist = sorted(((value, key) for (key, value) in temp.items()), reverse=True)
        sortdict = dict([(k, v) for v, k in templist])

        for key in sortdict:
            achievements += f"**{re_format(sortdict[key])}** {key}"

        if achievements == "":
            achievements = "None. Use `/submit` to submit a run."
        stats.description = achievements

        stats.set_author(name=member.name, icon_url=member.display_avatar.url)

        await ctx.followup.send(username="Vnav.io Personal Bests", embed=stats)

        end_time = self.time.time()
        print(
            f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds"
        )


def setup(bot):
    bot.add_cog(Profile(bot))
