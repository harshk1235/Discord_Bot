import discord 
from discord.ext import commands
from datetime import timedelta
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot=bot
    
    @app_commands.command()
    async def timeout(self, interaction:discord.Interaction, member :discord.Member, minutes: int, *, reason : str):
        """Timeouts a member for specified time"""
        delta = timedelta(minutes=minutes)
        await member.timeout(delta, reason=reason)
        await interaction.response.send_message(f"{member} has been timeout for {minutes} minutes")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))