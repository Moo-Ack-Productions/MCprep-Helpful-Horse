import discord
from discord.ext import tasks
import json
import datetime
import re

MCPREP_GUILD_ID       = 737871405349339232
IDLE_MINER_CHANNEL_ID = 746745594458144809
STAFF_CHAT_ID         = 741151005688987769

HTTPS = "https://"
HTTP  = "http://"

DISCORD_HTTPS = ("https://discord.com/", "https://cdn.discordapp.com/", "https://canary.discord.com/")

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

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
        message_content = message.content
        message_author = message.author
        if message_author.bot:
            return
        
        elif message.channel.id == IDLE_MINER_CHANNEL_ID:
            return
        
        if len(self.spam_text):
            if self.spam_text.count((message_author, message_content)) >= 3:
                for channel in message.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        try:
                            await message.channel.purge(limit=5, check=lambda x: (message_content in x.content) and x.author.id == message_author.id)
                        except Exception:
                            continue
                await message.channel.send(f"I said no spamming {message_author.mention}")
                await message_author.timeout_for(duration=datetime.timedelta(hours=5), reason="Spamming")
                
                if message.guild.id == MCPREP_GUILD_ID:
                    await self.staff_chat.send(f"{message_author} spammed this message \"{message_content}\"")
                
                
            if self.spam_text.count((message_author, message_content)) == 1:
                await message.channel.send(f"No spamming {message_author.mention}")
                
        if HTTPS in message_content or HTTP in message_content:
            for i in DISCORD_HTTPS:
                if i in message_content:
                    return
            if findWholeWord("free")(message_content) and findWholeWord("nitro")(message_content):
                try:
                    await message.delete()
                except Exception as e:
                    print(e)
                await message.channel.send(f"{message_author.mention}, for the safety of everyone here, I will mute you. Free nitro links are not allowed as 99% of the time they're scams")
                await message_author.timeout_for(duration=datetime.timedelta(hours=5), reason="Sending a free nitro link")
                await self.staff_chat.send(f"{message_author} sent this message \"{message_content}\"")
                return
            self.spam_text.append((message_author, message_content)) # append the author and message
        
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

@client.slash_command(name="mcprep_kaion", guilds=[MCPREP_GUILD_ID])
async def mcprep_kaion(ctx):
    await ctx.respond("MCprep Kaion is a fork of MCprep created by <@668304274580701202> with the goal of at least one update per month (though often times there's more than one update).\n\nKaion is only recommended for users that understand how to do proper bug reports and are willing to sacrafice a bit of stability for new features\n\nIt can be found: https://github.com/StandingPadAnimations/MCprep-Kaion")
    
@client.slash_command(name="blender_download", guilds=[MCPREP_GUILD_ID])
async def blender_download(ctx):
    await ctx.respond("Blender can be downloaded here: https://www.blender.org/")

@client.slash_command(name="my_hardware_sucks", guilds=[MCPREP_GUILD_ID])
async def my_hardware_sucks(ctx):
    await ctx.respond("Hardware does not matter in the beginning, whoever said that to you was lying.\n\nAll you need to get into 3D rendering is a computer, Blender, some time, and imagination.")
    
@client.slash_command(name="asset_submission", guilds=[MCPREP_GUILD_ID])
async def asset_submission(ctx):
    await ctx.respond("You can submit mob rigs here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=enhancement&template=Asset-Submission.yaml")

@client.slash_command(name="bug_report", guilds=[MCPREP_GUILD_ID])
async def bug_report(ctx):
    await ctx.respond("Submit a bug report here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=user-troubleshoot&template=Bug-Report.yml")
    
@client.slash_command(name="feature_request", guilds=[MCPREP_GUILD_ID])
async def feature_request(ctx):
    await ctx.respond("Submit a feature request here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=enhancement&template=Feature-Request.yml")

@client.slash_command(name="mojang_style", guilds=[MCPREP_GUILD_ID])
async def mojang_style(ctx):
    await ctx.respond("The \"Mojang Style\" is also known as barebones. All you need is the barebones texturepack and practice.")

@client.slash_command(name="why_is_standard_bad", guilds=[MCPREP_GUILD_ID])
async def why_is_standard_bad(ctx):
    images = None
    with open('assets/images.json') as f:
        data = json.load(f)
        images = data["why_not_to_use_standard"]
    
    RESPONSE_1 = f"Standard was designed a really long time ago, so it's really bad in terms of dynamic range. This makes areas blown out such as the rays of light in the bottom image:\n{images[0]}"
    RESPONSE_2 = f"You should use filmic instead, as it was designed with a higher dynamic range in mind. As you can see, the rays aren't blown out:\n {images[1]}\n\nOf course Filmic can look more washed out sometimes, but this can be fixed by setting the \"Look\" setting to \"High Contrast\""
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2)
    
@client.slash_command(name="why_is_my_cycles_render_so_noisy", guilds=[MCPREP_GUILD_ID])
async def why_is_my_render_griany(ctx):
    images = None
    with open('assets/images.json') as f:
        data = json.load(f)
        images = data["cycles_noise"]
    
    RESPONSE_1 = f"Cycles is a path tracing engine, so it produces very accurate lighting. A side effect of this is noise. At low samples it looks really bad:\n{images[0]}"
    RESPONSE_2 = f"As the number of samples increase, the clearer the image becomes:\n{images[1]}"
    RESPONSE_3 = f"There is a tool called denoising which helps with this problem (as seen in the bottom image):\n{images[2]}"
    RESPONSE_4 = f"It can be enabled here. It's recommended to use OpenImage Denoise as it preserves detail better:\n{images[3]}"
    RESPONSE_5 = "Remember this piece of advice though: denoisers are not magic. With low sample counts artifacts can appear that look like oil paint smudges."
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2)
    await ctx.respond(RESPONSE_3)
    await ctx.respond(RESPONSE_4)
    await ctx.respond(RESPONSE_5)
    
@client.slash_command(name="how_to_make_rtx_like_render", guilds=[MCPREP_GUILD_ID])
async def how_to_make_rtx_like_render(ctx):
    images = None
    with open('assets/images.json') as f:
        data = json.load(f)
        images = data["rtx_like_render"]
    
    RESPONSE_1 = f"You mean stuff like this?: {images[0]}\n{images[1]}"
    RESPONSE_2_1 = "The simple answer is time, blood, sweat, and tears. There's no magic button to instantly make good looking renders, it takes a lot of time, practice, and a willingness to learn. "
    RESPONSE_2_2 = "A common mistake people make is not willing to watch a tutorial because \"it doesn't match the blender version I'm using!\" or \"it's not related to Minecraft!\"\n\n"
    RESPONSE_2_3 = "The harsh reality is there is no easy path. You're going to have to learn by watching tutorials that are sometimes years old (Blender hasn't changed that much) or aren't remotely related to Minecraft. There is no easy path.\n\n"
    RESPONSE_2_4 = "In short, if you want to be good, you have to put in the work"
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2_1 + RESPONSE_2_2 + RESPONSE_2_3 + RESPONSE_2_4)
    
@client.slash_command(name="cycles_vs_eevee", guilds=[MCPREP_GUILD_ID])
async def cycles_vs_eevee(ctx):
    RESPONSE_1 = "Cycles is a path tracing engine, which means it properly simulates light. As a result, it creates stunning renders, but those renders come at the cost of render time and noise (use the `why_is_my_cycles_render_so_noisy` command for more info)\n\n"
    RESPONSE_2 = "EEVEE is a rasterized engine, which means it uses some crazy math to fake lighting. This means EEVEE has better performance, but the renders don't look as good compared to Cycles. In order to get something comparable, you need to do stuff such as baking indirect lighting, using reflection probes to improve reflections, etc.\n\n"
    RESPONSE_3 = "EEVEE does have one advantage though: NPR rendering such as anime or toon style rendering. Since EEVEE fakes its lighting, it's able to do things such as taking a shader input as a RGB mask, which makes EEVEE very powerful in the NPR world"
    RESPONSE_4 = "As for which engine is better, it depends. If by that question you meant \"Which engine is the best overall?\", then Cycles will always be better. If you meant \"Which engine is better for my style?\", that's for you to figure out on your own. If your style uses realistic lighting, then Cycles is your best bet. If your style doesn't need realistic lighting, then EEVEE may be a good option\n\n"
    RESPONSE_5 = "Sidenote: Before Blender 3.0, EEVEE was also much better in terms of volumetrics as they looked decent without taking eternity to render. However as of 3.0+, Cycles volumetrics have improved massively and now look much better then EEVEE's volumetrics"
    await ctx.respond(RESPONSE_1 + RESPONSE_2 + RESPONSE_3)
    await ctx.respond(RESPONSE_4 + RESPONSE_5)
    
@client.slash_command(name="please_use_google_next_time", guilds=[MCPREP_GUILD_ID])
async def please_use_google_next_time(ctx):
    RESPONSE_1 = "The people on this server are indeed very helpful and have good knowledge to share, but sometimes you can find the best answers even quicker by googling your question - especially if it's generic. You can always ask for more help here if you couldn't find what you wanted.\n"
    RESPONSE_2 = "Tip: Avoid using terms like \"minecraft animation\" when searching. You won't get much and all Blender concepts are easy to apply to Minecraft animation. Ex:\n"
    RESPONSE_3 = "Instead of this: \"How to attach objects to a minecraft rig in Blender\"\nDo this: \"How to attach objects to a rig in Blender\"\nYou'll get more search results that way"
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2 + RESPONSE_3)
    
@client.slash_command(name="optifine_shaders_in_blender", guilds=[MCPREP_GUILD_ID])
async def optifine_shaders_in_blender(ctx):
    RESPONSE_1 = "Optifine shaders can not be used in Blender, regardless if you're using MCprep or not. Optifine shaders were designed for the Optifine rendering pipeline, which does not exist in Blender and will never exist in Blender. If you wanted an easy way to do fancy lighting in Blender, then use the `how_to_make_rtx_like_render` command which will give you the harsh reality (apologies in advanced).\n\n"
    RESPONSE_2 = "Blender does have \"shaders\" though. You might know them as nodes (they're normally refered to as shader nodes).\n\n"
    await ctx.respond(RESPONSE_1 + RESPONSE_2)

@client.slash_command(name="shaders", guilds=[MCPREP_GUILD_ID])
async def shaders(ctx):
    RESPONSE_1 = "If by shaders you meant Optifine shaders, please use the `optifine_shaders_in_blender` command for info on why that's not possible.\n\n"
    RESPONSE_2 = "From a technical standpoint, a shader is a program that's ran on a CPU or GPU that does anything related to graphics. In fact, vanilla Minecraft uses shaders even with the default lighting, they're just not as fancy."
    await ctx.respond(RESPONSE_1 + RESPONSE_2)
    
@client.slash_command(name="previewing_animation_slow", guilds=[MCPREP_GUILD_ID])
async def previewing_animation_slow(ctx):
    await ctx.respond("Make sure you're using solid mode and not material or render mode for previewing animation")

@client.slash_command(name="unrealistic_expectations", guilds=[MCPREP_GUILD_ID])
async def unrealistic_expectations(ctx):
    await ctx.respond("Your expectations are too unrealistic")

@client.slash_command(name="world_exporter_issue", guilds=[MCPREP_GUILD_ID)
async def world_exporter_issue(ctx):
    await ctx.respond("The thing you've mentioned is something that would need to be done on the world exporter side first. We depend on world expoerer developers to do what we need to do, and they depend on us and othe r users to suggest features. For example, biome colors would require something exported by world exporters since all biome information is lose when exported")
    
@client.slash_command(name="blender_27x", guilds=[MCPREP_GUILD_ID])
async def blender_27x(ctx):
    await ctx.respond("Please upgrade from Blender 2.7x as soon as possible as it's extremely outdated. If you need to transition from 2.7x, then use Bforartists and set the keybinds to 2.7x at startup: https://www.bforartists.de/")
    
if __name__ == "__main__":
    token = None
    with open('config.json') as f:
        data = json.load(f)
        token = data["token"]
    client.run(token)
