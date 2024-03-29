from discord.ext import commands
from discord import Cog


class Event(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, msg1, msg):
        if "://" in msg.content.lower() and (
            "discord" in msg.content.lower()
            or "gift" in msg.content.lower()
            or "nitro" in msg.content.lower()
            or "free" in msg.content.lower()
        ):
            if (
                "support.discord.com"
                or "discord.gift"
                or "discord.com"
                or "discord.com/gift" in msg.content.lower()
            ):
                return
            await msg.delete()

    @Cog.listener()
    async def on_message(self, msg):
        if "://" in msg.content.lower() and (
            "discord" in msg.content.lower()
            or "gift" in msg.content.lower()
            or "nitro" in msg.content.lower()
            or "free" in msg.content.lower()
        ):
            if (
                "support.discord.com"
                or "discord.gift"
                or "discord.com"
                or "discord.com/gift" in msg.content.lower()
            ):
                return
            await msg.delete()


def setup(bot):
    bot.add_cog(Event(bot))
