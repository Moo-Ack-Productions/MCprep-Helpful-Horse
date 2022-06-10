import discord
from discord.ext import tasks
import json

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        
        # intents
        intents = discord.Intents.default()
        intents.message_content = True
        discord.Client.__init__(self, intents=intents)
        
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

if __name__ == "__main__":
    token = None
    with open('config.json') as f:
        data = json.load(f)
        token = data["token"]
    client = MyClient()
    client.run(token)