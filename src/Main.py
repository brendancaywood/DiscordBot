from discord.ext.commands import Bot
from collections import defaultdict
import asyncio
import discord

#the prefix used to signify commands
BOT_PREFIX = ('!')

#the bot itself
bot = Bot(command_prefix=BOT_PREFIX)

#the client
client = discord.Client()

#dictionary used to hold the members and their number of tallies
tallydict = {}

#the list that holds the owned games for an individual user
ownedGames = defaultdict(list)

#the list of members in the discord
members = []

#members matched with their usernames
usernameMemberDict = {}

#displayname matched with members
displaynameMemberDict = {}



"""
Runs at launch of the bot
"""
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

"""
Used to make the displaynameMemberDict and also the usernameMemberDict
"""
def userDict():

    #iterates all members of the discords and adds them to a list
    for member in bot.get_all_members():
        if member not in members:
            members.append(member)

    #iterates through and links members to their nicknames(displaynames)
    for username in members:
        if username.nick != None:
            usernameMemberDict[username] = username.nick
        else:
            usernameMemberDict[username] = username.name

    #iterates through the members and nicknames and makes a dictionary of nicknames and their members
    for uName, dName in usernameMemberDict.items():
        displaynameMemberDict[dName] = uName

"""
Command used to add tallies to a Member
@param desUser str the desired nickname to add the tally(s) to
@param num int the number of tallies to add to the member
"""
@bot.command(name='addTally',
                description="Adds a tally",
                brief="git roasted",
                aliases=['tally', 'addtally', 'Addtally'],
                pass_context=True)
async def addTally(ctx, desUser: str, num: int):
    #updates each of the user dictionaries for the latest values
    userDict()

    #check if the given nickname exists in the list of nicknames
    if desUser in usernameMemberDict.values():

        #grabs the key value combo from the displayname dictionary
        for dName, uName in displaynameMemberDict.items():
            if dName == desUser:
                if num == None:
                    num = 1
                if uName.name + '#' + uName.discriminator in tallydict:
                    tallydict[uName.name + '#' + uName.discriminator] += num
                    await ctx.send(desUser + ' now has ' + str(tallydict[uName.name + '#' + uName.discriminator]) + ' tallies.')
                else:
                    tallydict[uName.name + '#' + uName.discriminator] = num
                    await ctx.send(desUser + ' has recieved their first tally. They now have ' + str(tallydict[uName.name + '#' + uName.discriminator]) + ' tallies.')

@bot.command(name='getTallies',
                description="Gets number of Tallies",
                brief="git tallies",
                aliases=['gettally', 'getTally', 'Gettally', 'getTallies'],
                pass_context=True)
async def getTallies(ctx, desUser: str):
    userDict()
    if desUser in usernameMemberDict.values():
        for dName, uName in displaynameMemberDict.items():
            if dName == desUser:
                if uName.name + '#' + uName.discriminator in tallydict:
                    await ctx.send(desUser + ' has ' + tallydict(uName.name + '#' + uName.discriminator) + ' tallies.')
                else:
                    await ctx.send(desUser + ' has no tallies.')
@bot.command(name='addGame',
                description="Adds a Game to you Library",
                brief="add your game",
                aliases=['addgame', 'ADDGAME', 'Addgame'],
                pass_context=True)
async def addGame(ctx, desUser: str, game: str):
    userDict()
    if desUser in usernameMemberDict.values():
        for dName, uName in displaynameMemberDict.items():
            if dName == desUser:
                if uName.name + '#' + uName.discriminator in ownedGames:
                    gameSp = game + " "
                    ownedGames[uName.name + '#' + uName.discriminator].append(gameSp)
                    gameList = ''.join(ownedGames[uName.name + '#' + uName.discriminator])
                    msg = desUser + ' now has ' + gameList + 'games.'
                    await ctx.send(msg)
                else:
                    gameSp = game + " "
                    ownedGames[uName.name + '#' + uName.discriminator] = [gameSp]
                    gameList = ''.join(ownedGames[uName.name + '#' + uName.discriminator])
                    await ctx.send(desUser + ' has added their first game. They now have this ' + gameList + 'game.')

async def gameUpdate(ctx):
    await client.wait_until_ready()
    counter = 0
    for member in members:
        if member.name + '#' + member.discriminator in ownedGames:
            ownedGames[member.name + '#' + member.discriminator].append(member.game)
            gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
            msg = member.nick + ' now has ' + gameList + 'games.'
            await ctx.send(msg)
        else:
            ownedGames[member.name + '#' + member.discriminator] = [member.game]
            gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
            await ctx.send(member.nick + ' has added their first game. They now have this ' + gameList + 'game.')
    await asyncio.sleep(60) # task runs every 60 seconds