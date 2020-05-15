import asyncio
import discord
from discord.ext import commands, tasks

ffmpeg_options = {
    'options': '-vn'
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dance_loop = dance_loop

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel where I can DANCE"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def dance(self, ctx):
        """DANCE DANCE DANCE"""

        query = "dance"

        if not ".mp3" in query:
            query += ".mp3"

        v = ctx.voice_client
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        v.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        emb = discord.Embed(colour = discord.Colour.blurple(), title = "DANCE DANCE DANCE")
        await ctx.send(embed = emb)

        self.dance_loop.start(v, query)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the DANCE's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100

        emb = discord.Embed(description = "Changed volume to `{}%`".format(volume), colour = discord.Colour.blurple())
        await ctx.send(embed = emb)

    @commands.command()
    async def stop(self, ctx):
        """Stop dancing"""

        await ctx.voice_client.disconnect()

        emb = discord.Embed(description = "no more dance", colour = discord.Colour.blurple())
        await ctx.send(embed = emb)

    @dance.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("d/"), description='DANCE DANCE')
bot.remove_command("help")
bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print('ready as', bot.user)
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "D A N C E"))

@tasks.loop(seconds = 1)
async def dance_loop(voice_client, query):
    if voice_client.is_connected():
        if not voice_client.is_playing():
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
            voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    else:
        dance_loop.stop()

@bot.command(hidden = True)
async def help(ctx, *, command = None):
    "Get some dancing help"
    emb = discord.Embed(title = "Help!", colour = discord.Colour.blurple())
    emb.set_thumbnail(url = "https://data.whicdn.com/images/110985161/original.gif")
    if command:
        c = bot.get_command(command)
        if not c:
            emb = discord.Embed(description = "Nah, that's not a command", colour = discord.Colour.red())
            return await ctx.send(embed = emb)
        emb.description = f"**`{c.name} {c.signature}`**\n*{c.help}*"
        return await ctx.send(embed = emb)
    res = ""
    for a in bot.commands:
        if a.name != "jishaku":
            if not a.hidden:
                res += f"[**{a.name}**] {a.help}\n"
    emb.description = res
    await ctx.send(embed = emb)

@bot.command()
async def invite(ctx):
    "DANCE in your server"
    return await ctx.send(discord.utils.oauth_url(bot.user.id))

bot.add_cog(Music(bot))
bot.run('token')