from discord import ui, ButtonStyle, Embed, Color, InputTextStyle, Bot, Intents, SlashCommandGroup
from discord.ui import Modal, InputText
from time import time
from datetime import datetime
from replit import db

bot = Bot(intents=Intents.all())

Ships = ['Alien Blaster', 'Annihilator', 'Artillery', 'Artillery Shooter', 'Astronaut', 'Auto 4', 'Auto 5', 'Barricade', 'Basic', 'Bat', 'Bomber', 'Boomerang', 'Boomertwin', 'Booster', 'Boosterflip', 'Builder', 'Bushwacker', 'Carrier', 'Conqueror', 'Cruiser', 'Demolisher', 'Drone Addict', 'Drone Trapper', 'Dual', 'Factory', 'Fighter', 'Flank Guard', 'Fortress', 'Galaxian', 'Gunner', 'Gunner Trapper', 'Hulk', 'Hunter', 'Hybrid', 'Machine Gun', 'Mega 3', 'Necromancer', 'Octo Ship', 'Overbomber', 'Overboomerang', 'Overgunner', 'Overlord', 'Polyballs', 'Power Glider', 'Predator', 'Quad Ship', 'Quad-builder', 'Quadlet', 'Quintlet', 'Ranger', 'Savage', 'Skimmer', 'Sniper', 'Space Jet', 'Spike', 'Sprayer', 'Sputnik', 'Stradblock', 'Streamliner', 'Surfer', 'Trappershot', 'Trappetytrap', 'Triple Twin', 'Triplet', 'Twin Flank', 'Twin Laser', 'UFO']

ships1 = ['Alien Blaster', 'Annihilator', 'Artillery', 'Artillery Shooter', 'Astronaut', 'Auto 4', 'Auto 5']
ships2 = ['Barricade', 'Basic', 'Bat', 'Bomber', 'Boomerang', 'Boomertwin', 'Booster']
ships3 = ['Boosterflip', 'Builder', 'Bushwacker', 'Carrier', 'Conqueror', 'Cruiser', 'Demolisher']
ships4 = ['Drone Addict', 'Drone Trapper', 'Dual', 'Factory', 'Fighter', 'Flank Guard', 'Fortress']
ships5 = ['Galaxian', 'Gunner', 'Gunner Trapper', 'Hulk', 'Hunter', 'Hybrid', 'Machine Gun']
ships6 = ['Mega 3', 'Necromancer', 'Octo Ship', 'Overbomber', 'Overboomerang', 'Overgunner', 'Overlord']
ships7 = ['Polyballs', 'Power Glider', 'Predator', 'Quad Ship', 'Quad-builder', 'Quadlet', 'Quintlet']
ships8 = ['Ranger', 'Savage', 'Skimmer', 'Sniper', 'Space Jet', 'Spike', 'Sprayer']
ships9 = ['Sputnik', 'Stradblock', 'Streamliner', 'Surfer', 'Trappershot', 'Trappetytrap', 'Triple Twin']
ships10 = ['Triplet', 'Twin Flank', 'Twin Laser', 'UFO']

shipsall = [ships1, ships2, ships3, ships4, ships5, ships6, ships7, ships8, ships9, ships10]
modes = ["FFA","2 Teams"]

categories = ["Fast 500k", "Fast 1m", "Fast 1.5m", "High Score"]

ShipLower = [ship.lower() for ship in Ships]

places= ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Mobile 1st", "Mobile 2nd", "Mobile 3rd"]
placesPC = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
places_mobile = ["Mobile 1st", "Mobile 2nd", "Mobile 3rd"]

wr = SlashCommandGroup("worldrecords", "wr")

class ConfirmButton(ui.View):
  def __init__(self):
    super().__init__(timeout=60)
  

  @ui.button(label='Agree', style=ButtonStyle.green, emoji="✅")
  async def button_callback(self, button, interaction):
    self.stop()


class DenialReason(Modal):
    def __init__(self, message, ctx) -> None:
        super().__init__("Denial Reason")
        self.add_item(InputText(label="Why was this record denied?", placeholder="e.g. teaming, invalid score"))

        self.add_item(
            InputText(
                label="Additional Information",
                placeholder="Exactly where did this occur? Use complete sentences.",
                style=InputTextStyle.long,
                required=False,
                min_length=10
            )
        )
        
        self.message = message
        self.ctx = ctx

    async def callback(self, interaction):
        start_time = time()

        msg = self.message
        ctx = self.ctx

        embed = msg.embeds[0]
        embed.color = Color.brand_red()
        embed.timestamp = datetime.now()
        embed.set_footer(text="Denied at")
        
        await msg.edit(embed=embed)
        embed2 = Embed(title="Your submission has been denied...",url=msg.jump_url,color=Color.red())
        embed2.add_field(name="Reason",value=self.children[0].value)
        embed2.add_field(name="Details",value=self.children[1].value)
        try:
            author = db["submissions"][str(msg.id)]["author"]
        except KeyError:
            await interaction.response.send_message("Invalid submission!", ephemeral=True)
            return
        author = await bot.fetch_user(author)
        del(db["submissions"][str(msg.id)])

        try:
            await author.send(embed=embed2)
        except:
            pass
            
        await interaction.response.send_message("Denied...", ephemeral=True)
        end_time = time()
        print(f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds")
        
        return

class SubmissionForm(Modal):
    def __init__(self, ctx, ship, gamemode, platform) -> None:
        super().__init__("Vnav.io World Record Submission Form")
        self.add_item(InputText(label="Upload a link to a video of your gameplay:", placeholder="e.g. https://youtu.be/crazy-world-record"))
        self.add_item(InputText(label="Final score:", placeholder="e.g. 100000"))
        self.add_item(InputText(label="In-game hours:", placeholder="e.g. 1"))
        self.add_item(InputText(label="In-game minutes:", placeholder="e.g. 12"))
        self.add_item(InputText(label="In-game seconds:", placeholder="e.g. 23"))
        self.ctx = ctx
        self.ship = ship
        self.gamemode = gamemode
        self.platform = platform
        self.value = None

    async def callback(self, interaction):
        self.value = self.children
        evidence = self.value[0].value
        try:
            score = int(self.value[1].value)
            hours = int(self.value[2].value)
            minutes = int(self.value[3].value)
            seconds = int(self.value[4].value)
        except:
            await interaction.response.send_message("Invalid input!")
            
        ctx = self.ctx
        ship = self.ship
        gamemode = self.gamemode
        platform = self.platform

        start_time = time()
        if ship not in Ships:
            await interaction.response.send_message("Please select a valid ship.", ephemeral=True)
            return

        if "https://" not in evidence or " " in evidence:
            await interaction.response.send_message("You did not input a valid link as your evidence.", ephemeral=True)
            return
        
        if score < 100000:
            await interaction.response.send_message("World records need a minimal score of 100k.", ephemeral=True)
            return
        
        if (hours*3600)+(minutes*60)+(seconds) <= 10 or minutes > 60 or seconds > 60 or hours > 72:
            await interaction.response.send_message("You did not input a valid in-game time.", ephemeral=True)
            return

        print(f"[CALL] {ctx.interaction.user} passed checks for {ctx.command.name}")

        button = ConfirmButton()
        confirm = Embed(title="Submission", description="By submitting this as a world record, you have read and agree to the <#894470911623843871>.", color = Color.yellow())
        confirm.set_footer(text = "Allow a week for your submission to be reviewed.")
        await interaction.response.send_message(embed=confirm, view = button, ephemeral=True)

        ButtonTimeoutBool = await button.wait()
        for child in button.children:
            child.disabled = True
        TimedOut = Embed(title = "Session Timed-Out. Try again.", color = Color.red())
        Submit = Embed(title = "Your submission has been submitted. Awaiting approval...", color = Color.green())
        if ButtonTimeoutBool:
            await interaction.edit_original_message(embed = TimedOut, view = button)
            return
        
        await interaction.edit_original_message(embed = Submit, view = button)

        embed = Embed(title= f"{ship} ({gamemode}) ({platform})", color=Color.yellow(), url = evidence)
        embed.add_field(name="Score",value="{:,}".format(score))
        embed.add_field(name="Time",value=f"{hours}h {minutes}m {seconds}s")
        embed.add_field(name="Submitter",value=f"{ctx.author.mention}")
        embed.timestamp = datetime.now()
        embed.set_footer(text="Submitted at")
        channel = await ctx.guild.fetch_channel(915211422475108393)

        msg = await channel.send(embed=embed)
        db["submissions"][str(msg.id)] = {}
        db["submissions"][str(msg.id)]["author"] = ctx.author.id
        db["submissions"][str(msg.id)]["user"] = ctx.author.name
        db["submissions"][str(msg.id)]["ship"] = ship
        db["submissions"][str(msg.id)]["sec"] = seconds
        db["submissions"][str(msg.id)]["min"] = minutes
        db["submissions"][str(msg.id)]["hour"] = hours
        db["submissions"][str(msg.id)]["link"] = evidence
        db["submissions"][str(msg.id)]["score"] = score
        db["submissions"][str(msg.id)]["platform"] = platform
        db["submissions"][str(msg.id)]["gamemode"] = gamemode
        
        end_time = time()
        print(f"[CLOSE] {ctx.interaction.user} completed {ctx.command.name}. Runtime: {round(end_time - start_time)} seconds")