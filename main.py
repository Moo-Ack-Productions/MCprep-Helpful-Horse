import discord
import asyncio
import json

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spam_text = None
        self.token = None
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        discord.Client.__init__(self, intents=intents)
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if self.spam_text is not None:
            if message.content == self.spam_text:
                message.channel.send("no spamming!")
        self.spam_text = message.content
        await asyncio.sleep(100)
        self.spam_text = None

if __name__ == "__main__":
    token = None
    with open('config.json') as f:
        data = json.load(f)
        token = data["token"]
    client = MyClient()
    client.run(token)