from unicodedata import category
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.core import command
import nextcord
import pymongo
from pymongo import MongoClient
discord = nextcord

cluster = MongoClient("URL")
db = cluster["chatbot"]
collection = db["main"]
ticket_status = db["ticket_status"]


class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def closeticket(self, ctx):

        channel = ctx.channel
        try:
            query = {"ticket_id": channel.id}
            log = ticket_status.find(query)
            
            for result in log:
                ticket = result["ticket_id"]
            
            if ticket == channel.id:

                ticket_channel = nextcord.utils.get(ctx.channel.guild.text_channels, id=ticket)
                ticket_status.delete_one(query)
                await ticket_channel.delete()
        
        except:

            await ctx.send("**Please Run This Command In A Ticket**")


def setup(bot : commands.Bot):
    bot.add_cog(system(bot))