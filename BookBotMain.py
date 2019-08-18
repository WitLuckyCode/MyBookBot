#!/usr/bin/env python3
import discord
from discord.ext import commands
import BotRequests
from config import myToken

description = "A bot that searches for books via title/author/isbn"

bot = commands.Bot(command_prefix='b/', description=description)
bot.remove_command('help')

@bot.event
async def on_ready():
    game=discord.Game("b/help")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        title = 'Help',
        description = "A list of commands and what they do",
        colour = discord.Color.dark_green()
    )

    embed.add_field(name ="search", value="Search results for books via author/title or ISBN")
    await ctx.send(author, embed=embed)

@bot.command(pass_context=True)
async def search(ctx, *, args):
    emojiBack = "◀"
    emojiForw = "▶"
    qData = BotRequests.findBookByTitleAuthorISBN(args)#returns dict of first page of results
    #print(qData[0])
    #print(args)

    embed = discord.Embed(
        title = 'Results',
        description = "Search results for books via author/title or ISBN",
        colour = discord.Color.dark_green()
    )

    if len(qData) == 0: #if dict empty
        embed.set_author(name=args)
        embed.add_field(name="No Results", value="Nothing was found, maybe you miss-typed?", inline=False)
    else:
        embed.set_thumbnail(url='https://s.gr-assets.com/assets/icons/goodreads_icon_50x50-823139ec9dc84278d3863007486ae0ac.png')
        embed.set_image(url = f"{qData[0]['image']}")
        embed.set_author(name=args)
        embed.set_footer(text='Uses the goodreads api')
        embed.add_field(name='Title', value=f"{qData[0]['title']}", inline = True)
        embed.add_field(name='Author', value=f"{qData[0]['author']}", inline = True)
        embed.add_field(name ='Publication Date', value=f"{qData[0]['oriPubDay']}.{qData[0]['oriPubMonth']}.{qData[0]['oriPubYear']}", inline = True)
        embed.add_field(name='Book ID', value=f"{qData[0]['bookID']}", inline = True)
        embed.add_field(name='Ratings', value=f"Average rating of {qData[0]['rating']} out of {qData[0]['ratingCount']} ratings", inline = False)
        embed.add_field(name='Cover', value=f"{qData[0]['image']}", inline = False)
    
    addReact = await ctx.send(embed=embed)
    await addReact.add_reaction(emojiBack)
    await addReact.add_reaction(emojiForw)

# Get at discordapp.com/developers/applications/me    
bot.run(myToken)