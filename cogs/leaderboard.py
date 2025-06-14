import discord 
from discord import app_commands
from discord import message
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json 
import asyncio


google_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
google_creds = ServiceAccountCredentials.from_json_keyfile_name('discord-bot-420212-750895fd16bb.json', google_scope)
google_client = gspread.authorize(google_creds)

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    google_sheet_url = config_data.get('google_sheet_url', '')
   
sheet = google_client.open_by_url(google_sheet_url)
with open('emoji.json', 'r') as emoji_file:
    emoji_file = json.load(emoji_file)
    th17 = emoji_file.get('th17', '')
    th16 = emoji_file.get('th16', '')
    th15 = emoji_file.get('th15', '')
    th14 = emoji_file.get('th14', '')
    th13 = emoji_file.get('th13', '')
    th12 = emoji_file.get('th12', '')
    th11 = emoji_file.get('th11', '')
    th10 = emoji_file.get('th10', '')



class Data_entry(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot=bot
        self.last_embed_message = None
        self.bot.tree.add_command(self.leaderboard)
        self.bot.tree.add_command(self.refresh_leaderboard)
    
    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard(self, ctx: discord.Interaction, channel: discord.TextChannel = None):
        """Displays the leaderboard for the current season"""
        try:
            if channel is None:
                channel = ctx.channel
    
            stat_sheet = google_client.open_by_url(google_sheet_url).worksheet("War Stats")
            war_stats = stat_sheet.get_all_values()
            text = ""
            heading = "<:blank_space:1229767163221381173><:blank_space:1229767163221381173>`Atk \t Trp \t H/R% \t Dest`\n\n"
    
            for row in war_stats[1:]:
                if row[1] == '17':
                    emo = th17
                elif row[1] == '16':
                    emo = th16
                elif row[1] == '15':
                    emo = th15
                elif row[1] == '14':
                    emo = th14
                elif row[1] == '13':
                    emo = th13
                elif row[1] == '12':
                    emo = th12
                elif row[1] == '11':
                    emo = th11
                elif row[1] == '10':
                    emo = th10
                text += f"{emo}<:blank_space:1229767163221381173>`{row[2]:^3} \t {row[3]:^3} \t {row[4]:>3}% \t {row[5]:>4}`   \t {row[0]}\n" 
            embed = discord.Embed(title="🏆 War Leaderboard 🏆", description="\n **Greetings, Clashers!** \n\n Join us in celebrating the noble feats of our champions as we unveil the monthly leaderboard for Clash of Clans. \n\n" + heading + text, color=0x36bd9f)
            embed.set_footer(text="FoV", icon_url="https://media.discordapp.net/attachments/1228051187337527358/1232750588656357547/WhatsApp_Image_2024-04-11_at_22.32.41.jpeg?ex=662a97f3&is=66294673&hm=a56ed586c65e3ab38b3c62a60ea9f25ef3c754b7078be891f1a7282cdb1e1b71&=&format=webp&width=396&height=350")
            await ctx.response.send_message("Leaderboard sent!", ephemeral=True)
            self.last_embed_message = await channel.send(embed=embed)
            
        except Exception as e:
            await ctx.response.send_message("An error occurred while retrieving stats info")
    
    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def refresh_leaderboard(self, ctx: discord.Interaction, channel:discord.TextChannel):
        """Refreshes the leaderboard"""
        try:
            # Check if last_embed_message is available
            if self.last_embed_message:
                # Retrieve the message containing the leaderboard embed
                message = await ctx.channel.fetch_message(self.last_embed_message.id)
    
                # Check if the message is found
                if message:
                    # Retrieve the updated leaderboard data
                    stat_sheet = google_client.open_by_url(google_sheet_url).worksheet("War Stats")
                    war_stats = stat_sheet.get_all_values()
                    text = ""
                    heading = "<:blank_space:1229767163221381173><:blank_space:1229767163221381173>`Atk \t Trp \t H/R% \t Dest`\n\n"
    
                    for row in war_stats[1:]:
                        if row[1] == '17':
                            emo = th17
                        elif row[1] == '16':
                            emo = th16
                        elif row[1] == '15':
                            emo = th15
                        elif row[1] == '14':
                            emo = th14
                        elif row[1] == '13':
                            emo = th13
                        elif row[1] == '12':
                            emo = th12
                        elif row[1] == '11':
                            emo = th11
                        elif row[1] == '10':
                            emo = th10
                        text += f"{emo}<:blank_space:1229767163221381173>`{row[2]:^3} \t {row[3]:^3} \t {row[4]:>3}% \t {row[5]:>4}`   \t {row[0]}\n" 
                    embed = discord.Embed(title="🏆 War Leaderboard 🏆", description="\n **Greetings, Clashers!** \n\n Join us in celebrating the noble feats of our champions as we unveil the monthly leaderboard for Clash of Clans. \n\n" + heading + text, color=0x36bd9f)
                    embed.set_footer(text="FoV", icon_url="https://media.discordapp.net/attachments/1228051187337527358/1232750588656357547/WhatsApp_Image_2024-04-11_at_22.32.41.jpeg?ex=662a97f3&is=66294673&hm=a56ed586c65e3ab38b3c62a60ea9f25ef3c754b7078be891f1a7282cdb1e1b71&=&format=webp&width=396&height=350")
    
                    # Edit the existing message with the new embed
                    await ctx.response.send_message("Leaderboard refreshed successfully.", ephemeral=True)
                    await message.edit(embed=embed)
                    
                else:
                    await ctx.response.send_message("Unable to find the previous leaderboard message.", ephemeral=True)
            else:
                await ctx.response.send_message("There is no previous leaderboard to refresh.", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message("An error occurred while refreshing the leaderboard.")
        
    
        

 
async def setup(bot: commands.Bot):
    await bot.add_cog(Data_entry(bot))
