from tkinter import Button
from unicodedata import category
import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Button
from nextcord.ext.commands.core import command
import nextcord
import pymongo
from pymongo import MongoClient
discord = nextcord

cluster = MongoClient("URL")
db = cluster["chatbot"]
collection = db["main"]
ticket_status = db["ticket_status"]

class buttons_two(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None 

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)  
    async def yes(self, button : nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)  
    async def no(self, button : nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()


class main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):

        guild = ctx.channel.guild

        embed_second = nextcord.Embed(title="Setup", 
        description="Would you like to log all the modmail tickets created & deleted?"
        )
        embed_third = nextcord.Embed(title="Setup", 
        description="Setup Is Complete."
        )
        embed_fourth = nextcord.Embed(title="Setup", 
        description="Type the channel name you would like to have the embed where users create tickets."
        )
        create_ticket = nextcord.Embed(title="Create A Ticket", 
        description="Press the button below to create a ticket."
        )
            
        view_two = buttons_two()

        send = await ctx.send(embed=embed_second, view=view_two)
        await view_two.wait()

        if view_two.value == True:

            await send.edit(embed=embed_fourth, view=None)

            msg = await self.bot.wait_for("message", 
                        timeout=60, 
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                    )
            
            channel = nextcord.utils.get(guild.text_channels, name = msg.content)
            
            category = await guild.create_category("Tickets")
            log_channel = await guild.create_text_channel("log", category=category)

            query = {"guild" : guild.id, "category": category.id, "log_channel": log_channel.id}
            collection.insert_one(query)

            await send.edit(embed=embed_third, view=None)
            if channel is not None:
                
                view = View()
                button = Button(label="Create Ticket", style=discord.ButtonStyle.green)
                view.add_item(button)

                await channel.send(embed=create_ticket, view=view)

                async def button_callback(interaction):
                    close = View()
                    button = Button(label="Close", style=discord.ButtonStyle.red)
                    close.add_item(button)
                    
                    embed = nextcord.Embed(title="Close Ticket", description="React Below To Close The Ticket")

                    int_guild = interaction.channel.guild
                    try:
                        find_user = {"user_id": interaction.user.id}
                        log = ticket_status.find(find_user)
                        for result in log:
                            user = result["user_id"]

                        if user:
                            await interaction.channel.send("Ticket already created!")
                    
                    except:

                        find_guild = {"guild": int_guild.id}
                        log = collection.find(find_guild)
                        for result in log:

                            category = result["category"]
                    
                        category = nextcord.utils.get(int_guild.categories, id=category)
                        channel = await int_guild.create_text_channel("ticket", category=category)
                        
                        query = {"guild": int_guild.id, "user_id": interaction.user.id, "ticket_id": channel.id}
                        ticket_status.insert_one(query)

                        msg = await channel.send(embed=embed, view=close)

                        await msg.channel.set_permissions(interaction.user, 
                            read_messages=True, 
                            send_messages=True)
                        await msg.channel.set_permissions(ctx.guild.default_role, 
                            read_messages=False, 
                            send_messages=False)

                        async def callback(interaction):

                            channel = interaction.channel

                            await channel.delete()
                            query = {"ticket_id": channel.id}
                            ticket_status.delete_one(query)
                        
                        button.callback = callback

                
                button.callback = button_callback



        elif view_two.value == False:
                
            category = await guild.create_category("Tickets")

            query = {"guild" : guild.id, "category": category.id, "log_channel": "Nill"}
            collection.insert_one(query)

            await send.edit(embed=embed_third, view=None)

def setup(bot : commands.Bot):
    bot.add_cog(main(bot))