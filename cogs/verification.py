from discord import message_command, Color, Embed
from discord.ext.commands import Cog
from constants import bot, placesPC, places_mobile, DenialReason
from time import time
from datetime import datetime
from replit import db

class Verification(Cog):
    
    def __init__(self, bot):
        super().__init__()

    @message_command(name="deny", guild_ids=[588921569271611393])
    async def deny(ctx, msg):
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
        
        try:
            author_id = db["submissions"][str(msg.id)]["author"]
        except KeyError:
            await ctx.followup.send("This has already been approved!")
        
        ship, seconds, minutes, hours, evidence, score, platform, gamemode = db["submissions"][str(msg.id)]["ship"], db["submissions"][str(msg.id)]["sec"], db["submissions"][str(msg.id)]["min"],db["submissions"][str(msg.id)]["hour"], db["submissions"][str(msg.id)]["link"], db["submissions"][str(msg.id)]["score"], db["submissions"][str(msg.id)]["platform"], db["submissions"][str(msg.id)]["gamemode"]
        IGtimesec = (seconds) + (minutes*60) + (hours*3600)
        
        mobile = False if platform == "PC" else True
        
        arry = {author_id:{"author_id":author_id, "score":score, "evidence":evidence, "hours":hours, "minutes":minutes, "seconds":seconds, "mobile":mobile}}
        
        if str(author_id) not in db["personal best"]:
            db["personal best"][str(author_id)] = []
    
        db["personal best"][str(author_id)].append({})
        db["personal best"][str(author_id)][0]["ship"] = ship
        db["personal best"][str(author_id)][0]["link"] = evidence
        db["personal best"][str(author_id)][0]["gamemode"] = gamemode
        db["personal best"][str(author_id)][0]["hours"] = hours
        db["personal best"][str(author_id)][0]["minutes"] = minutes
        db["personal best"][str(author_id)][0]["seconds"] = seconds
        db["personal best"][str(author_id)][0]["score"] = score
        
        categories = ["High Score"]
        
        if score >= 500000:
            categories.append("Fast 500k")
        if score >= 1000000:
            categories.append("Fast 1m")
        if score >= 1500000:
            categories.append("Fast 1.5m")
        
        for author in arry.copy():
            for category in categories:
                IGtimesec = (arry[author]["seconds"]) + (arry[author]["minutes"]*60) + (arry[author]["hours"]*3600)
        
            if arry[author]["mobile"]:
                for place in places_mobile:
                    if db[ship][gamemode][category][place]["user"] == 0:
                        db[ship][gamemode][category][place]["user"] = f'{author_id}|{score}'
                        db[ship][gamemode][category][place]["link"] = evidence
                        db[ship][gamemode][category][place]["hour"] = hours
                        db[ship][gamemode][category][place]["min"] = minutes
                        db[ship][gamemode][category][place]["sec"] = seconds
                        break
        
                    elif "Fast" in category:
                        time_ = ((db[ship][gamemode][category][place]["sec"]) + (db[ship][gamemode][category][place]["min"]*60) + (db[ship][gamemode][category][place]["hour"]*3600))
                        if IGtimesec < time_:
                            author_score = db[ship][gamemode][category][place]["user"]
                            author_id2 = author_score.split("|")[0]
                            score2 = author_score.split("|")[1]
        
                            evidence2 = db[ship][gamemode][category][place]["link"]
                            hours2 = db[ship][gamemode][category][place]["hour"]
                            minutes2 = db[ship][gamemode][category][place]["min"]
                            seconds2 = db[ship][gamemode][category][place]["sec"]
                            
                            arry.update({author_id2:{"author_id":author_id2, "score":score2, "evidence":evidence2, "hours":hours2, "minutes":minutes2, "seconds":seconds2, "mobile": True}})
                            IGtimesec = (seconds2) + (minutes2*60) + (hours2*3600)
        
                            db[ship][gamemode][category][place]["user"] = f'{arry[author]["author_id"]}|{arry[author]["score"]}'
                            db[ship][gamemode][category][place]["link"] = arry[author]["evidence"]
                            db[ship][gamemode][category][place]["hour"] = arry[author]["hours"]
                            db[ship][gamemode][category][place]["min"] = arry[author]["minutes"]
                            db[ship][gamemode][category][place]["sec"] = arry[author]["seconds"]
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
                            
                            arry.update({author_id2:{"author_id":author_id2, "score":score2, "evidence":evidence2, "hours":hours2, "minutes":minutes2, "seconds":seconds2, "mobile": True}})
        
                            db[ship][gamemode][category][place]["user"] = f'{arry[author]["author_id"]}|{arry[author]["score"]}'
                            db[ship][gamemode][category][place]["link"] = arry[author]["evidence"]
                            db[ship][gamemode][category][place]["hour"] = arry[author]["hours"]
                            db[ship][gamemode][category][place]["min"] = arry[author]["minutes"]
                            db[ship][gamemode][category][place]["sec"] = arry[author]["seconds"]
                            break
                    
            for place in placesPC: #not mobile / is mobile
        
                if db[ship][gamemode][category][place]["user"] == 0:
                    db[ship][gamemode][category][place]["user"] = f'{author_id}|{score}'
                    db[ship][gamemode][category][place]["link"] = evidence
                    db[ship][gamemode][category][place]["hour"] = hours
                    db[ship][gamemode][category][place]["min"] = minutes
                    db[ship][gamemode][category][place]["sec"] = seconds
                    break
        
                elif "Fast" in category:
                    time_ = ((db[ship][gamemode][category][place]["sec"]) + (db[ship][gamemode][category][place]["min"]*60) + (db[ship][gamemode][category][place]["hour"]*3600))
                    if IGtimesec < time_:
                        author_score = db[ship][gamemode][category][place]["user"]
                        author_id2 = author_score.split("|")[0]
                        score2 = author_score.split("|")[1]
        
                        evidence2 = db[ship][gamemode][category][place]["link"]
                        hours2 = db[ship][gamemode][category][place]["hour"]
                        minutes2 = db[ship][gamemode][category][place]["min"]
                        seconds2 = db[ship][gamemode][category][place]["sec"]
                        
                        arry.update({author_id2:{"author_id":author_id2, "score":score2, "evidence":evidence2, "hours":hours2, "minutes":minutes2, "seconds":seconds2, "mobile": False}})
                        IGtimesec = (seconds2) + (minutes2*60) + (hours2*3600)
        
                        db[ship][gamemode][category][place]["user"] = f'{arry[author]["author_id"]}|{arry[author]["score"]}'
                        db[ship][gamemode][category][place]["link"] = arry[author]["evidence"]
                        db[ship][gamemode][category][place]["hour"] = arry[author]["hours"]
                        db[ship][gamemode][category][place]["min"] = arry[author]["minutes"]
                        db[ship][gamemode][category][place]["sec"] = arry[author]["seconds"]
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
                        
                        arry.update({author_id2:{"author_id":author_id2, "score":score2, "evidence":evidence2, "hours":hours2, "minutes":minutes2, "seconds":seconds2, "mobile": False}})
        
                        db[ship][gamemode][category][place]["user"] = f'{arry[author]["author_id"]}|{arry[author]["score"]}'
                        db[ship][gamemode][category][place]["link"] = arry[author]["evidence"]
                        db[ship][gamemode][category][place]["hour"] = arry[author]["hours"]
                        db[ship][gamemode][category][place]["min"] = arry[author]["minutes"]
                        db[ship][gamemode][category][place]["sec"] = arry[author]["seconds"]
                        break
        
        del(db["submissions"][str(msg.id)])
        embed = msg.embeds[0]
        embed.color = Color.green()
        embed.timestamp = datetime.now()
        embed.set_footer(text="Approved at")
        id = 929206223037952050
        ping = ctx.guild.get_role(id)
        await ctx.followup.send("Approved!")
        await ctx.send(f"{ping.mention} New World Record Approved!")
        await msg.edit(embed=embed)
        embed2 = Embed(title="Your submission has been approved!",url=msg.jump_url,color=Color.green())
        author = await bot.fetch_user(author_id)
        try:
            await author.send(embed=embed2)
        except:
            pass
        
        end_time = time()
        print(f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds")
        
        return

def setup(bot):
    bot.add_cog(Verification(bot))