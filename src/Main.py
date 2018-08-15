from discord.ext.commands import Bot
from collections import defaultdict

BOT_PREFIX = ('!')
bot = Bot(command_prefix=BOT_PREFIX)
tallydict = {}
ownedGames = defaultdict(list)
members = []
usernameMemberDict = {}
displaynameMemberDict = {}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')


def userDict():
    for member in bot.get_all_members():
        if member not in members:
            members.append(member)

    for username in members:
        if username.nick != None:
            usernameMemberDict[username] = username.nick
        else:
            usernameMemberDict[username] = username.name

    for uName, dName in usernameMemberDict.items():
        displaynameMemberDict[dName] = uName
    print(displaynameMemberDict)


@bot.command(name='addTally',
                description="Adds a tally",
                brief="git roasted",
                aliases=['tally', 'addtally', 'Addtally'],
                pass_context=True)
async def addTally(ctx, desUser: str, num: int):
    userDict()
    if desUser in usernameMemberDict.values():
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

@bot.command(name='addGame',
                description="Adds a Game to you Library",
                brief="add your game",
                aliases=['addgame', 'ADDGAME', 'Addgame'],
                pass_context=True)
async def addGame(ctx, desUser: str, game: str):
    if desUser in ownedGames:
        gameSp = game + " "
        ownedGames[desUser].append(gameSp)
        gameList = ''.join(ownedGames[desUser])
        msg = desUser + ' now has ' + gameList + 'games.'
        await ctx.send(msg)
    else:
        gameSp = game + " "
        ownedGames[desUser] = [gameSp]
        gameList = ''.join(ownedGames[desUser])
        await ctx.send(desUser + ' has added their first game. They now have this ' + gameList + 'game.')

