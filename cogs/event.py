from discord.ext.commands import Cog
from discord.ext import commands

class Event(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, msg1,msg):
        if "://" in msg.content.lower() and ("discord" in msg.content.lower() or "gift" in msg.content.lower() or "nitro" in msg.content.lower() or "free" in msg.content.lower()):
            if "support.discord.com" or "discord.gift" or "discord.com" or "discord.com/gift" in msg.content.lower():
                return
            await msg.delete()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if "://" in msg.content.lower() and ("discord" in msg.content.lower() or "gift" in msg.content.lower() or "nitro" in msg.content.lower() or "free" in msg.content.lower()):
            if "support.discord.com" or "discord.gift" or "discord.com" or "discord.com/gift" in msg.content.lower():
                return
            await msg.delete()
    
        if msg.author.id == 586743480651350063 and msg.content == "/reload":
            m = await msg.reply(
                "Syncing code..."
            )
            for ext in ['cogs.submit', 'cogs.wr', 'cogs.profile', 'cogs.event', 'cogs.verification']:
                self.bot.reload_extension(ext)
            await m.edit("Code has been synced.")
            commands = ""
            for app in self.bot.walk_application_commands():commands += f"{app.qualified_name}"
            await msg.channel.send(commands)

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(f"[INIT] {interaction.user} issued a {interaction.type}")
        await self.bot.process_application_commands(interaction)
    
def setup(bot):
    bot.add_cog(Event(bot))
    