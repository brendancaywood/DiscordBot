from discord.ext.commands import Bot
from collections import defaultdict
import asyncio

"""
A discord bot with various different purposes

@author Brendan Caywood
"""
# the prefix used to signify commands
BOT_PREFIX = '!'

# the bot itself
bot = Bot(command_prefix=BOT_PREFIX)

# dictionary used to hold the members and their number of tallies
tallydict = {}

# the list that holds the owned games for an individual user
ownedGames = defaultdict(list)

# the list of members in the discord
members = []

# members matched with their usernames
usernameMemberDict = {}

# displayname matched with members
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
    #gets updated list of members and their related usernames/nicknames
    userDict()


"""
Used to make the displaynameMemberDict and also the usernameMemberDict
"""


def userDict():
    # iterates all members of the discords and adds them to a list
    for member in bot.get_all_members():
        if member not in members:
            members.append(member)
    # iterates through and links members to their nicknames(displaynames)
    for username in members:
        if username.nick is not None:
            usernameMemberDict[username] = username.nick
        else:
            usernameMemberDict[username] = username.name
    # iterates through the members and nicknames and makes a dictionary of nicknames and their members
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
    # updates each of the user dictionaries for the latest values
    userDict()

    # check if the given nickname exists in the list of nicknames
    if desUser in usernameMemberDict.values():

        # grabs the key value combo from the displayname dictionary
        for dName, uName in displaynameMemberDict.items():

            # figures out the correct displayname from the list
            if dName == desUser:
                if num == None:
                    num = 1
                if uName.name + '#' + uName.discriminator in tallydict:
                    tallydict[uName.name + '#' + uName.discriminator] += num
                    await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' now has ' + str(
                        tallydict[uName.name + '#' + uName.discriminator]) + ' tallies.')
                else:
                    tallydict[uName.name + '#' + uName.discriminator] = num
                    await bot.send_message(bot.get_channel('478974569558966286'),
                                           desUser + ' has received their first tally. They now have ' + str(
                                               tallydict[uName.name + '#' + uName.discriminator]) + ' tallies.')
    else:
        await bot.send_message(bot.get_channel('478974569558966286'), "Please input a valid name(case sensitive)")

"""
Command used to get the number of tallies for a Member
@param desUser str the desired nickname to get the tally(s) from
"""


@bot.command(name='getTallies',
             description="Gets number of Tallies",
             brief="git tallies",
             aliases=['gettally', 'getTally', 'Gettally'],
             pass_context=True)
async def getTallies(ctx, desUser: str):
    # gets updated list of members and their related usernames/nicknames
    userDict()
    if desUser in usernameMemberDict.values():
        for dName, uName in displaynameMemberDict.items():
            if dName == desUser:
                if uName.name + '#' + uName.discriminator in tallydict:
                    await ctx.send(desUser + ' has ' + tallydict[uName.name + '#' + uName.discriminator] + ' tallies.')
                else:
                    await ctx.send(desUser + ' has no tallies.')
    else:
        await bot.send_message(bot.get_channel('478974569558966286'), "Please input a valid name(case sensitive)")

"""
Command used to manually add a game to a member
@param desUser str the desired nickname to add the game(s) to
@param game str the game to add to the member
"""


@bot.command(name='addGame',
             description="Adds a Game to you Library",
             brief="add your game",
             aliases=['addgame', 'ADDGAME', 'Addgame'],
             pass_context=True)
async def addGame(ctx, desUser: str, game: str):
    # gets updated list of members and their related usernames/nicknames
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

"""
Automatic task used to grab what games each user is playing
and add it to their list of games if applicable
"""


async def gameUpdate():
    await bot.wait_until_ready()
    # gets updated list of members and their related usernames/nicknames
    userDict()
    for member in members:
        print("1")
        if member.game is not None:
            if member.name + '#' + member.discriminator in ownedGames:
                if member.game.name not in ownedGames[member.member.name + '#' + member.discriminator]:
                    ownedGames[member.name + '#' + member.discriminator].append(member.game.name)
                    gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
                    msg = member.nick + ' now has ' + gameList + 'games.'
                    await bot.send_message(bot.get_channel('478974569558966286'), msg)
            else:
                ownedGames[member.name + '#' + member.discriminator] = [member.game.name]
                gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
                await bot.send_message(bot.get_channel('478974569558966286'),
                                       member.nick + ' has added their first game. They now have this ' + member.game.name + ' game.')
    await asyncio.sleep(1)  # task runs every 60 seconds


bot.loop.create_task(gameUpdate())
