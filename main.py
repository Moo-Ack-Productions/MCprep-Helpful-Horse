import discord
from discord.ext import tasks
import json
import datetime

MCPREP_GUILD_ID       = 737871405349339232
IDLE_MINER_CHANNEL_ID = 746745594458144809
STAFF_CHAT_ID         = 741151005688987769

HTTPS = "https://"
HTTP  = "http://"

DISCORD_HTTPS = ("https://discord.com/", "https://cdn.discordapp.com/", "https://canary.discord.com/")

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
        
        self.staff_chat = self.get_channel(STAFF_CHAT_ID)
        
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        elif message.channel.id == IDLE_MINER_CHANNEL_ID:
            return
        
        if len(self.spam_text):
            if self.spam_text.count((message.author, message.content)) >= 3:
                for channel in message.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        try:
                            await channel.purge(limit=5, check=lambda x: (message.content in x.content) and x.author.id == message.author.id)
                        except Exception:
                            continue
                await message.channel.send(f"I said no spamming {message.author.mention}")
                await message.author.timeout_for(duration=datetime.timedelta(hours=5), reason="Spamming")
                
                if message.guild.id == MCPREP_GUILD_ID:
                    await self.staff_chat.send(f"{message.author} spammed this message \"{message.content}\"")
                
                
            if self.spam_text.count((message.author, message.content)) == 1:
                await message.channel.send(f"No spamming {message.author.mention}")
                
        if HTTPS in message.content or HTTP in message.content:
            for i in DISCORD_HTTPS:
                if i in message.content:
                    return
            self.spam_text.append((message.author, message.content)) # append the author and message
        
    @tasks.loop(minutes=5)
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

@client.slash_command(name="why_is_standard_bad", guilds=[MCPREP_GUILD_ID])
async def why_is_standard_bad(ctx):
    images = None
    with open('assets/images.json') as f:
        data = json.load(f)
        images = data["why_not_to_use_standard"]
    
    RESPONSE_1 = f"Standard was designed a really long time ago, so it's really bad in terms of dynamic range. This makes areas blown out such as the rays of light in the bottom image:\n{images[0]}"
    RESPONSE_2 = f"You should use filmic instead, as it was designed with a higher dynamic range in mind. As you can see, the rays aren't blown out:\n {images[1]}"
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2)

if __name__ == "__main__":
    token = None
    with open('config.json') as f:
        data = json.load(f)
        token = data["token"]
    client.run(token)