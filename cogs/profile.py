from discord.commands import user_command
from discord.ext.commands import Cog
import discord
from replit import db
from rounding import re_format
import time

class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = time
    
    @user_command(name="Profile", guild_ids=[588921569271611393], default_permission=True)
    async def profile(self, ctx, member) -> None:
        db2, achievements = db, ""

        temp = {}
        stats = discord.Embed(title="Personal Best", color=ctx.guild.me.color)
        
        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")
        start_time = self.time.time()
        
        await ctx.defer(ephemeral=True)
        
        try:
            db2["personal best"][str(member.id)]
        except:
            achievements = "None. Use `/submit` to submit a run."
        
            stats.description=achievements
            stats.set_author(name = member.name)
            
            await ctx.followup.send(embed=stats)
            end_time = self.time.time()
            print(f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds")
            return
            
        a = db2["personal best"][str(member.id)]
        
        for score in a: 
            
            ship, mode, link, score1 = score["ship"], score["gamemode"], score["link"], int(score["score"])
            if score["hours"] == 0:
                
                sec = f'0{score["seconds"]}' if len(str(score["seconds"])) == 1 else f'{score["seconds"]}'
                
                time = f"{score['minutes']}:{sec}"
            else:

                sec = f'0{score["seconds"]}' if len(str(score["seconds"])) == 1 else f'{score["seconds"]}'

                min = f'0{score["minutes"]}' if len(str(score["minutes"])) == 1 else f'{score["minutes"]}'
                
                time = f"{score['hours']}:{min}:{sec}"

            if not(f"[{ship} {time} ({mode})]" in temp):

                temp[f"[{ship} {time} ({mode})]({link})\n"] = score1


        templist=sorted(((value, key) for (key,value) in temp.items()), reverse=True)
        sortdict=dict([(k,v) for v,k in templist])

        for key in sortdict:
            achievements += f"**{re_format(sortdict[key])}** {key}"
        
        if achievements == "": achievements = "None. Use `/submit` to submit a run."
        stats.description = achievements
        
        stats.set_author(name = member.name, icon_url = member.display_avatar.url)
        
        await ctx.followup.send(username="Vnav.io Personal Bests", embed=stats)
        
        end_time = self.time.time()
        print(f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds")

def setup(bot):
    bot.add_cog(Profile(bot))