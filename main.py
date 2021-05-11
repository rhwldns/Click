from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=['ㅊ.', 'c.', 'ㅊ. ', 'c. '], help_command=None)


if __name__ == "__main__":
    file_list_py = [file for file in os.listdir('./cogs') if file.endswith(".py")]
    for i in file_list_py:
        bot.load_extension(str(i))


@bot.event
async def on_ready():
    print(f'[Log - System] {bot.user} On Ready.')
    

bot.run(os.getenv("TOKEN"))