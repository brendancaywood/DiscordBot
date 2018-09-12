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

#List of games
games = []

#the current server of the bot
server = bot.get_server()

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
async def addTally(ctx, desUser: str, num: int = 1):
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
                    await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' has ' + str(tallydict[uName.name + '#' + uName.discriminator]) + ' tallies.')
                else:
                    await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' has no tallies.')
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

    if game is not None and desUser is not None:
        if desUser in usernameMemberDict.values():
            for dName, uName in displaynameMemberDict.items():
                if dName == desUser:
                    if uName.name + '#' + uName.discriminator in ownedGames:
                        gameSp = game + " "
                        ownedGames[uName.name + '#' + uName.discriminator].append(gameSp)
                        gameList = ''.join(ownedGames[uName.name + '#' + uName.discriminator])
                        msg = desUser + ' now has ' + gameList + 'games.'
                        await bot.send_message(bot.get_channel('478974569558966286'), msg)

                    else:
                        gameSp = game + " "
                        ownedGames[uName.name + '#' + uName.discriminator] = [gameSp]
                        gameList = ''.join(ownedGames[uName.name + '#' + uName.discriminator])
                        await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' has added their first game. They now have this ' + gameList + 'game.')
        else:
            await bot.send_message(bot.get_channel('478974569558966286'), "Please input a valid name(case sensitive)")

"""
Command used to get the number of tallies for a Member
@param desUser str the desired nickname to get the tally(s) from
"""


@bot.command(name='getGames',
             description="Gets the list of games",
             brief="git games",
             aliases=['getgame', 'getGame', 'Getgame', 'getgames'],
             pass_context=True)
async def getGames(ctx, desUser: str):
    # gets updated list of members and their related usernames/nicknames
    userDict()
    if desUser in usernameMemberDict.values():
        for dName, uName in displaynameMemberDict.items():
            if dName == desUser:
                if uName.name + '#' + uName.discriminator in ownedGames:
                    await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' has these games: ' + ownedGames[uName.name + '#' + uName.discriminator])
                else:
                    await bot.send_message(bot.get_channel('478974569558966286'), desUser + ' has no games.')
    else:
        await bot.send_message(bot.get_channel('478974569558966286'), "Please input a valid name(case sensitive)")


"""
Automatic task used to grab what games each user is playing
and add it to their list of games if applicable
"""


async def userGameUpdate():
    await bot.wait_until_ready()
    while not bot.is_closed:
        print("Checking for new games...")

        # gets updated list of members and their related usernames/nicknames
        userDict()

        # loops through and grabs each member
        for member in members:

            # checks if nickname is nothing, if it is set it to normal name
            if member.nick is None:
                member.nick = member.name

            # see if they are playing a game
            if member.game is not None:
                rolesUpdate(member.game.name)
                # check if they already have a game
                if member.name + '#' + member.discriminator in ownedGames:

                    # if the game hasn't already been added
                    if member.game.name not in ownedGames[member.name + '#' + member.discriminator]:
                        ownedGames[member.name + '#' + member.discriminator].append(str(member.game.name))
                        gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
                        msg = member.nick + ' now has these games: ' + gameList
                        await bot.send_message(bot.get_channel('478974569558966286'), msg)
                else:
                    ownedGames[member.name + '#' + member.discriminator] = str(member.game.name)
                    gameList = ''.join(ownedGames[member.name + '#' + member.discriminator])
                    await bot.send_message(bot.get_channel('478974569558966286'), member.nick + ' has added their first game. They now have this ' + gameList + ' game.')
        await asyncio.sleep(60)  # task runs every 60 seconds

"""
Checks if anyone is playing a game that currently isn't listed
"""
def rolesUpdate(name):
    print(server.roles)
    if name not in games:
        games.append(name)

bot.loop.create_task(userGameUpdate())
