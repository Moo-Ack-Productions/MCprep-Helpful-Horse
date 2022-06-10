import discord
from discord.ext import tasks
import json

MCPREP_GUILD_ID = 737871405349339232

class MyClient(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        
        # intents
        intents = discord.Intents.default()
        intents.message_content = True
        discord.Bot.__init__(self, intents=intents)
        
        # the magic behind the whole thing
        self.spam_text = []
        self.reset_spam_text.start()
        
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if len(self.spam_text):
            if self.spam_text.count((message.author, message.content)) > 3:
                await message.channel.send("I said no spamming {message.author.mention}")
                await message.guild.ban(message.author, reason="Caught spamming by helpful horse")
                
            if self.spam_text.count((message.author, message.content)):
                await message.channel.send(f"No spamming {message.author.mention}")
        self.spam_text.append((message.author, message.content)) # append the author and message
        
    @tasks.loop(hours=24)
    async def reset_spam_text(self):
        self.spam_text = []
        
    @reset_spam_text.before_loop
    async def initionalize(self):
        await self.wait_until_ready()

client = MyClient()

@client.slash_command(name="mcprep_download", guilds=[MCPREP_GUILD_ID])
async def mcprep_download(ctx):
    await ctx.respond("MCprep can be downloaded here: https://github.com/TheDuckCow/MCprep/releases")
    
@client.slash_command(name="blender_download", guilds=[MCPREP_GUILD_ID])
async def blender_download(ctx):
    await ctx.respond("Blender can be downloaded here: https://www.blender.org/")
    
@client.slash_command(name="where_do_i_submit_assets", guilds=[MCPREP_GUILD_ID])
async def asset_submission(ctx):
    await ctx.respond("You can submit mob rigs here: https://github.com/TheDuckCow/MCprep/issues/245")

if __name__ == "__main__":
    token = None
    with open('config.json') as f:
        data = json.load(f)
        token = data["token"]
    client.run(token)