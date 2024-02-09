from discord_components import Button, DiscordComponents
import googlesearch
from serpapi import GoogleSearch
from discord.ext import commands
import cv2
import discord
import random

client = commands.Bot(command_prefix="!")
DiscordComponents(client)
page = 1


@client.event
async def on_ready():
    print("Bot online")


@client.command()
async def hey(ctx):
    name = ctx.author.name
    await ctx.send(f"Hey, {name}!")


@client.command()
async def coffee(ctx):
    responses = ["No, make it yourself, you little bitch.",
                 "I'm too busy to be making coffee for your lazy ass.",
                 "Sure, if you want it thrown at your dumb face",
                 "What happened? Fucking wanker can't even make a coffee for itself"]
    await ctx.send(random.choice(responses))


@client.command()
async def die(ctx):
    await ctx.send("Bye!")
    await client.close()


@client.command()
async def shit(ctx, member: discord.Member):
    print("Done")
    Image = cv2.imread("shit.png")
    print("not")
    text = member.display_name
    text_pos = (250, 750)
    print(text)
    cv2.putText(Image, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite("temp_img.png", Image)
    await ctx.send(file=discord.File("temp_img.png"))


@client.command(brief="Displays weather")
async def weather(ctx, *, location=''):
    params = {
        "engine": "google",
        "q": f"weather{location}",
        "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
    }
    search = GoogleSearch(params).get_dict()
    results = search['answer_box']

    answer_embed = discord.Embed(title="Search Result",
                                 description=f"Temperature: {results['temperature']}\nPrecipitation: {results['precipitation']}\nHumidity: {results['humidity']}\nWind: {results['wind']}")
    await ctx.send(embed=answer_embed)


@client.command(brief="Displays news")
async def news(ctx, *, title=''):
    if title != '':
        for i in googlesearch.search(title, num=1, stop=1):
            await ctx.send(str(i))
        return

    global page
    params = {
        "engine": "google",
        "q": "news",
        "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    def display(start=0, end=8):
        global page
        if page == 2:
            page = 1
        else:
            page += 1
        if end < len(results['top_stories']):
            disp = [(i['title'], i['date'], i['source']) for i in results['top_stories'][start:end]]
        else:
            disp = [(i['title'], i['date'], i['source']) for i in results['top_stories'][start:len(results['top_stories'])]]
        news_embed = discord.Embed(title="News")
        for data in disp:
            news_embed.add_field(name=data[0], value=f"{data[1]}\nsource: {data[2]}")
        return news_embed

    await ctx.send(embed=display(), components=[Button(emoji="⏬", style=3, custom_id="page_next")])

    while True:
        interaction = await client.wait_for("button_click", check= lambda i: i.custom_id == "page_back")
        await interaction.send(embed=display(8*(page-1), 8*page), components=[Button(emoji="⏫", style=3, custom_id="page_back")], ephemeral=False)


@client.command(brief="Defines a word", aliases=["word", "def", "meaning", "dict"])
async def define(ctx, *, word):
    if word.strip() == "annoying":
        await ctx.send(embed=discord.Embed(title='an·noy·ing', description="(adjective)\n\n1. You"))
        return
    params = {
        "engine": "google",
        "q": f"{word} meaning",
        "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
    }
    search = GoogleSearch(params).get_dict()
    result = search['answer_box']

    def list_maker():
        out = "\n"
        for i in list(enumerate([''] + result['definitions']))[1:]:
            out += f"\t{i[0]}. {i[1]}\n"
        return out

    if result['type'] == "organic_result":
        word_embed = discord.Embed(title=word, description=result['title'])
    elif result['type'] == "dictionary_results":
        word_embed = discord.Embed(title=result['syllables'], description=f"({result['word_type']})\n{list_maker()}")
    else:
        await ctx.send("Check if you entered that correctly.")
        return

    await ctx.send(embed=word_embed)


@client.command(aliases=['q', 'w'], brief="Ask any question")
async def ques(ctx, *, query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
    }
    search = GoogleSearch(params)
    try:
        results = search.get_dict()["answer_box"]
    except:
        try:
            results = search.get_dict()["knowledge_graph"]
        except:
            results = search.get_dict()
            print(results)

    try:
        answer_embed = discord.Embed(title=results["title"], description=results['answer'])
    except:
        try:
            answer_embed = discord.Embed(title=results["title"], description=results['description'])
        except:
            answer_embed = discord.Embed(title=results["title"], description=results['snippet'])
    await ctx.send(embed=answer_embed)


@client.command(aliases=["distance"], brief="How many ITEMS between two places")
async def dist(ctx, *, rem):
    rem = rem.lower()
    item, places = rem.split('between')
    orig, dest = places.split('and')
    it_dic = {
        "miles": 0.621371,
        "yards": 1093.61,
        "feet": 3280.84,
        "bread": 4374.45556,
        "bread loaves": 4374.45555556,
        "inches": 39370.1,
        "centimetres": 100000,
        "metres": 1000
    }
    if item.strip() not in it_dic:
        await ctx.send("Item selected is unrecognised!")
        return
    params = {
        "engine": "google",
        "q": f"how far away is {dest} from {orig}",
        "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
    }
    results = GoogleSearch(params).get_dict()
    print(results)
    try:
        distance = [i for i in results['organic_results'][0]['snippet'].split() if i.isdigit()]
    except:
        distance = [i for i in results['answer_box']['snippet'].split() if i.isdigit()]

    distance_km = int(distance[0])
    distance_km *= it_dic[item.strip()]

    answer_embed = discord.Embed(title=f"Distance Between {orig} and {dest}", description=f"{distance_km} {item}")
    await ctx.send(embed=answer_embed)


@client.command(alias="img", brief="Displays an image")
async def image(ctx, *, query):
    params = {"engine": "google",
              "tbm": "isch",
              "q": f"{query}",
              "api_key": "ccd9a1006808391a57c5491d6add75a35452e5fec719866c6ba724dc94010a67"
              }
    search = GoogleSearch(params).get_dict()
    results = [i['original'] for i in search["images_results"][:3]]

    img_embed = discord.Embed(title="Image search results")
    img_embed.set_image(url=results[0])
    #img_embed.set_footer(icon_url=results[1], text=" ")
    img_embed.set_thumbnail(url=results[2])
    await ctx.send(embed=img_embed)


client.run('ODk5MjA2MTM2MTY1Njk5NTk0.GRzoxw.-jHWCIRiinHOLlHFoKM9naA-QGwc88KEHTnBWw')
