from nextcord.ext import commands
from nextcord.shard import EventItem
from nextcord import Intents
import nextcord

bot_version = '0.0.2'

# Client
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix='.', help_commmand=None, intents=intents)
bot.remove_command('help')

extensions = [
    'Cogs.modmail',
    'Cogs.commands'
    ]   
if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)

# Startup
@bot.event
async def on_ready():
    print("Bot Ready")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Yes"))

bot.run('TOKEN')