
from youtube_search import YoutubeSearch
import discord
from discord.ext import commands
from discord import app_commands
from discord import Intents # I could have imported all in one line, but I like doing it in multiples lines more
import json
import requests
import random
import time
import not_so_useful_things as ImUsefulISwear
guild_id = 982963585749758032
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

Prefix = "<" #you need to declare a prefix to run the bot in order to be able to change the prefix - Who made this ?
TOKEN = '' #should be in a .env file, but I cba to make one rn, so ima just delete it for github :D


for k in range(0, 50):
    smeaning = str(ImUsefulISwear.s_meaning[(random.randint(0, len(ImUsefulISwear.s_meaning)-1))])
    bmeaning = str(ImUsefulISwear.b_meaning[(random.randint(0, len(ImUsefulISwear.b_meaning)-1))])
    qmeaning = str(ImUsefulISwear.q_meaning[(random.randint(0, len(ImUsefulISwear.q_meaning)-1))])
    print("sbq mean "+smeaning+" "+bmeaning+" "+qmeaning+" !")


boopCooldowns = {}
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=Prefix, intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=guild_id)) #remove the id part for a public server - see the first cmd for more info
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


bot = Bot()
bot.remove_command('help') #who want a non working /help cmd ?

@bot.event
async def on_ready(): #that's your code, almost nothing changed
        with open('serverConfig.json', 'r') as file:
            config_data = json.load(file)

        # Get a list of server IDs from the loaded configuration
        configured_servers = list(config_data['server'].keys())

        # Iterate over the guilds your bot is in
        for guild in bot.guilds:
            guild_id = str(guild.id)

            # Check if the server ID is already present in the configuration
            if guild_id not in configured_servers:
                # Add the server ID to the configuration with default values
                config_data['server'][guild_id] = {
                    "prefix": "<",
                    "server_permissions": ["ADMINISTRATOR", "MANAGE_GUILD"],
                }


        # Remove server entries from the configuration if the bot is not in those servers
        for server_id in configured_servers:
            if not any(guild.id == int(server_id) for guild in bot.guilds):
                del config_data['server'][server_id]
                print(f"Removed server with ID {server_id} from the configuration.")

        # Save the updated configuration back to the JSON file
        with open('serverConfig.json', 'w') as file:
            json.dump(config_data, file, indent=4)

        with open('serverConfig.json') as file:
                json_data = file.read()
                jsonPrefixList = json.loads(json_data)
                Prefix = jsonPrefixList["server"][(str(guild.id))]["prefix"]
                bot.command_prefix = Prefix
@bot.event
async def on_guild_join(guild):
    with open('serverConfig.json', 'r') as file:
        with open('serverConfig.json', 'r') as file:
            config_data = json.load(file)

        # Get a list of server IDs from the loaded configuration
        configured_servers = list(config_data['server'].keys())

        # Iterate over the guilds your bot is in
        for guild in bot.guilds:
            guild_id = str(guild.id)

            # Check if the server ID is already present in the configuration
            if guild_id not in configured_servers:
                # Add the server ID to the configuration with default values
                config_data['server'][guild_id] = {
                    "prefix": "<",
                    "server_permissions": ["ADMINISTRATOR", "MANAGE_GUILD"],
                }

        # Remove server entries from the configuration if the bot is not in those servers
        for server_id in configured_servers:
            if not any(guild.id == int(server_id) for guild in bot.guilds):
                del config_data['server'][server_id]
                print(f"Removed server with ID {server_id} from the configuration.")

        # Save the updated configuration back to the JSON file
        with open('serverConfig.json', 'w') as file:
            json.dump(config_data, file, indent=4)

        with open('serverConfig.json') as file:
                json_data = file.read()
                jsonPrefixList = json.loads(json_data)
                Prefix = jsonPrefixList["server"][(str(guild.id))]["prefix"]
                bot.command_prefix = Prefix
        new_nickname = f"SBQUtil [{Prefix}]"  # Replace with the desired nickname
        try:
            for guild in bot.guilds:
                await guild.me.edit(nick=new_nickname)
        except discord.Forbidden:
            print("no perm to change name")



# command that work both with prefix and as a /cmd -> only here for testing purpose tbh
@bot.hybrid_command(name="isalive", with_app_command=True, description="check if the bot is dead or not")
@app_commands.guilds(discord.Object(id=guild_id)) #sync the command to only 1 server to be much faster (need to disable it for a public bot, however new command might take up to a day to register)
#@commands.has_permissions(administrator=True) #decorator to check for admin perm, you can check for every perm with it (this cmd won't work without admin perm, if turned to false no one will be able to run it)
async def isalive(ctx: commands.Context):
    await ctx.defer(ephemeral=False) #set to true if only the user of the command should see the message
    await ctx.reply("I am indeed alive, thank for asking.")




#at first I wanted to store them in another file, using the built in function from discord-py, but for some reason it was eating my memory so I had to put everything in the same file in order to fix the memory leak



@bot.hybrid_command(name="reload", description="reload the config file, shouldn't be needed (require admin perm)") #whenever the command is called it will load again the config (should also be ran  after a prefix change)
@app_commands.guilds(discord.Object(id=guild_id))
@commands.has_permissions(administrator=True)
async def reload(ctx):
    await ctx.send("reloaded the config")
    with open('serverConfig.json') as file:
            json_data = file.read()
            jsonPrefixList = json.loads(json_data)
            Prefix = jsonPrefixList["server"][(str(ctx.guild.id))]["prefix"]
            bot.command_prefix = Prefix

@bot.hybrid_command(name="w", description="search the wiki")
@app_commands.guilds(discord.Object(id=guild_id))
async def w(ctx, *, query): #do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the * do not forget the *
    arg1 = query
    officialWiki = requests.get(
        'https://wiki.hypixel.net/index.php?title=Special:Search&search=' + arg1,
        allow_redirects=True).url
    fanWiki = 'https://hypixel-skyblock.fandom.com/wiki/Special:Search?search=' + arg1.replace(' ', '_')
    if officialWiki.__contains__("index"):
        answer = f'Page not found! Fan wiki the search link: <{fanWiki}>'
    else:
        answer = officialWiki
    await ctx.reply(answer)

@bot.hybrid_command(name="g", description="search on google")
@app_commands.guilds(discord.Object(id=guild_id))
async def g(ctx, *, query): #letmegooglethat cmd
        answer = '<https://letmegooglethat.com/?q=' + query.replace(' ', '+') + '>'
        await ctx.send(answer) #using send instead of reply as you usualy use "letmegooglethat" for other, not for yourself

@bot.hybrid_command(name="s", description="pull a skycrypt profile [showing skyblock stat]") #at some point ima fail to type "description"
@app_commands.guilds(discord.Object(id=guild_id))
async def s(ctx, ign):
    if ign == None:
        await ctx.reply("usage : /s [IGN]")
    else:
        if ign == "supermagister18":
            ign = "DeathStreeks"
        elif ign == "supermagister17":
            ign = "supermagister18"
        answer = 'https://sky.shiiyu.moe/stats/' + ign
        await ctx.reply(answer)

@bot.hybrid_command(name="nmc", description="pull a name mc link")
@app_commands.guilds(discord.Object(id=guild_id))
async def nmc(ctx, ign):
   answer = 'https://namemc.com/search?q=' + ign
   await ctx.reply(answer)

@bot.hybrid_command(name="namemc", description="pull a name mc link") #duplicate of the above command, could have made a function for it but a copy past work, and is faster to run since im using decorator
@app_commands.guilds(discord.Object(id=guild_id))
async def namemc(ctx, ign):
   answer = 'https://namemc.com/search?q=' + ign
   await ctx.reply(answer)

@bot.hybrid_command(name="pl", description="pull a plancke.io [showing hypixel stat] link for the following ign") #from now on im copy pasting "description".
@app_commands.guilds(discord.Object(id=guild_id))
async def pl(ctx, ign):
   answer = 'https://plancke.io/hypixel/player/stats/' + ign
   await ctx.reply(answer)

@bot.hybrid_command(name="plancke", description="pull a plancke.io [showing hypixel stat] link for the following ign") #also a duplicate,still can't make an allias
@app_commands.guilds(discord.Object(id=guild_id))
async def plancke(ctx, ign):
   answer = 'https://plancke.io/hypixel/player/stats/' + ign
   await ctx.reply(answer)

@bot.hybrid_command(name="r", description="choose between multiple option, separated by either a comma [,] or a space [ ]")
@app_commands.guilds(discord.Object(id=guild_id))
async def r(ctx, choices):
    c = str(choices)
    c = c.replace(","," ")
    c = c.split()
    n = len(c)
    answer = c[random.randint(0, n-1)]
    await ctx.reply("I chose : "+answer)

@bot.hybrid_command(name="boop", description="BOOP, boop boop, boop !")
@app_commands.guilds(discord.Object(id=guild_id))
async def boop(ctx, target):
    timeRn = time.time()
    authorId = ctx.author.id
    target = str(target).replace("<@","")
    target = target.replace(">", "") #get rid of the <@[id]> to keep only the id
    if authorId != 561533536218382347: #don't delete my cd bypass ty, if you want you can also add your id to be able to bypass !
        if authorId in boopCooldowns and timeRn - boopCooldowns[authorId] < 300:
            # User is on cooldown, return a user_message indicating when they can use the command again
            remaining_time = int(300 - (timeRn - boopCooldowns[authorId]))
            await ctx.reply(f'<@{authorId}> This command is on cooldown for {remaining_time}.')
        else:
            # User is not on cooldown, update the cooldown dictionary and execute the command
            boopCooldowns[authorId] = timeRn
            answer = f'<@{target}> <:hypixelboop:809950751819563020>'
            await ctx.send(answer)
    else:
        answer = f'<@{target}> <:hypixelboop:809950751819563020>'
        await ctx.send(answer)

@bot.hybrid_command(name="prefix", description="change the prefix of the bot, require admin perm to do so.")
@app_commands.guilds(discord.Object(id=guild_id))
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix):
    server_id = ctx.guild.id
    with open('serverConfig.json', 'r') as file:
        data = json.load(file)
        if len(new_prefix) >= 4:
            await ctx.reply("the prefix is limited to 3 characters")
        else:
            Prefix = new_prefix
            bot.command_prefix = Prefix

            with open('serverConfig.json', 'r') as file:
                    data = json.load(file)

                # Update the prefix for the server ID
            if str(server_id) in data['server']: #shouldn't be needed, work as a failsafe in case the server isn't in the config for some reason
                    if new_prefix == data['server'][str(server_id)]['prefix']:
                        await ctx.reply(f"Prefix is already {new_prefix}")
                    else:
                        await ctx.reply(f'''The new prefix is: {Prefix}''')
                    data['server'][str(server_id)]['prefix'] = new_prefix
            else:
                    await ctx.reply("Error")

                # Save the updated JSON data back to the file
            with open('serverConfig.json', 'w') as file:
                json.dump(data, file, indent=4)
                file.close()

                new_nickname = f"SBQUtil [{new_prefix}]"  # Replace with the desired nickname
            try:
                for guild in bot.guilds:
                        await guild.me.edit(nick=new_nickname)
            except discord.Forbidden:
                await ctx.reply("Insufficient permissions to change nickname.")

@bot.hybrid_command(name="leave", description="make the bot leave the server. need admin perm.") #accidentaly kicked my bot twice because I forgot to change the cmd name after copy pasting it !
@app_commands.guilds(discord.Object(id=guild_id))
@commands.has_permissions(administrator=True)
async def leave(ctx):
    guild = ctx.guild
    await ctx.reply("Fine, I will leave by myself :'(")
    await guild.leave()

@bot.hybrid_command(name="mcuuid", description="send the minecraft uuid of the player") #accidentaly kicked my bot twice because I forgot to change the cmd name after copy pasting it !
@app_commands.guilds(discord.Object(id=guild_id))
async def mcuuid(ctx, ign):
    api_url = f'https://api.mojang.com/users/profiles/minecraft/{ign}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        uuid = data.get('id')
        await ctx.reply(f"The UUID of player '{ign}' is: {uuid}")
    else:
        await ctx.reply(f"Player '{ign}' not found or an error occurred.")

@bot.hybrid_command(name="joke", description="tell you a joke (don't blame me if it's not funny !)") #most useful command so far #yes, this basicaly tell a joke (or what the theorem of fermat is, about once every 103 jokes)
@app_commands.guilds(discord.Object(id=guild_id))
async def joke(ctx):
    joke_list = ImUsefulISwear.gpt_joke #powered by chatGPT !
    n = random.randint(0, len(joke_list))
    answer = str(joke_list[n])
    if ctx.author.id != 550857166697922570: #this is bourbon id, since he always ask math question it will have a chance of rolling exclusive jokes from the math pool !
        await ctx.reply(answer)
    else:
        k = random.randint(0, 1)
        if k == 0:
            answer = str(ImUsefulISwear.math_joke[random.randint(0, len(ImUsefulISwear.math_joke)-1)])
            await ctx.reply(answer)


@bot.hybrid_command(name="rolecount", description="count the amount of user with a role (don't ask me why this command exist).") #bot seem to only itself as a member, even if the members intents is on
@app_commands.guilds(discord.Object(id=guild_id)) #had the same issue when parsing player roles to get manager perm, if you get it to work feel free to add the manager perm system back (and delete the admin perm decorator)
async def rolecount(ctx, role_name):
    server = bot.get_guild(ctx.guild.id)
    num=0
    for member in server.members:
        print(member) #used to debug, print every member it can see (it seems to only show itself, even with members intent enabled
        for role in member.roles:
            #print(role.name) #used to debug, show every role of a member (since it's in a loop it will show the roles of every member)
            if role.name == role_name:
                num=num+1

    await ctx.reply(num)

@bot.hybrid_command(name="yt", description="search for a youtube video")
@app_commands.guilds(discord.Object(id=guild_id))
async def yt(ctx, *,query):
    search_query = str(query)
    results = YoutubeSearch(search_query, max_results=1).to_dict()
    if results:
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
        await ctx.reply(f"{video_url}")
    else:
        await ctx.reply(f"No search results found for '{search_query}'.")


@bot.hybrid_command(name="help", description="return a list of command and what they do.")
@app_commands.guilds(discord.Object(id=guild_id))
async def help(ctx):
    Prefix = bot.command_prefix
    embedVar = discord.Embed(title="SBQUtil Help Menu"
                             , description="[Denotes mandatory argument] (Denotes optional argument)"
                             , color=0x00fff)
    embedVar.add_field(name=f"{Prefix}help"
                       , value="Shows this message."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}yt [query]", value="search the inputed query on youtube")
    embedVar.add_field(name=f"{Prefix}w [Search phrase]"
                       , value="Links to the Hypixel Wiki with inputted search phrase."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}g [Search phrase]"
                       , value="Links to Let Me Google That with inputted search phrase."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}s [Minecraft IGN]"
                       , value="Links to SkyCrypt with inputted IGN."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}namemc [Minecraft IGN]"
                       , value="Links to NameMC with inputted IGN, shortcut : "f"{Prefix}nmmc [Minecraft IGN]."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}plancke [Minecraft IGN]"
                       , value="send a plancke.io [showing hypixel stat] link for the following ign, shortcut : "f"{Prefix}pl [Minecraft IGN]"
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}r [option 1], [option 2], (etc.)"
                       , value="Randomly chooses an option from inputted options, separated by either a comma [,] or a space [ ]."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix}boop [User ID]"
                       , value="Boops user (5 minute cooldown, either ping the user or input his id in the user id field)."
                       , inline=False)
    embedVar.add_field(name=f"{Prefix} mcuuid [ign]", value="give the uuid of the player.")
    embedVar.add_field(name=f"{Prefix}isalive", value="check if the bot is alive, more to be added soonTM")
    embedVar.add_field(name="ADMIN COMMAND", value="command below this line require admin perm.", inline=False)
    embedVar.add_field(name=f"{Prefix} reload", value="reload the config, shouldn't be needed, only use it if the bot doesn't recognise a custom prefix after a reboot.")
    embedVar.add_field(name=f"{Prefix} prefix [new prefix]", value="change the prefix needed to run the command (slash command will still work regardless of what you put here). Defaut prefix : < ", inline=False)
    embedVar.add_field(name=f"{Prefix} leave", value="make the bot leave the server by itself. This command is a thing because after talking with the bot we noticed that he hated to get kicked out of a server, and that if he is unwanted he would rather leave by itself")
    embedVar.set_footer(text="SBQUtil Bot, made by supermagister18 and 45gd !")
    await ctx.reply(embed=embedVar)


bot.run(TOKEN) #now it's no longer spaghetti code, it's perfectly cooked spaghetti :D
