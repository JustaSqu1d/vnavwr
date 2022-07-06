from constants import Ships, SubmissionForm
from discord.commands import Option
from discord.utils import basic_autocomplete
from discord import slash_command, Cog


class Submit(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="submit",
        description="Submit your world record attempts here.",
        guild_ids=[588921569271611393],
    )
    async def submit(
        self,
        ctx,
        ship: Option(
            str,
            "Which ship are you submitted a record for?",
            autocomplete=basic_autocomplete(Ships),
        ),
        gamemode: Option(
            str,
            "Which gamemode did you play this in?",
            choices=["FFA", "2 Teams"],
            required=True,
        ),
        platform: Option(
            str,
            "Did you play this on mobile or PC?",
            choices=["PC", "Mobile"],
            required=True,
        ),
    ):

        modal = SubmissionForm(ctx, ship, gamemode, platform)
        await ctx.interaction.response.send_modal(modal)


def setup(bot):
    bot.add_cog(Submit(bot))
