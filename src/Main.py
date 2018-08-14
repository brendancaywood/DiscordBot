from discord.ext.commands import Bot
from collections import defaultdict

BOT_PREFIX = ('!')
bot = Bot(command_prefix=BOT_PREFIX)
tallydict = {}
ownedGames = defaultdict(list)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

@bot.event
async def on_message(message):
    for member in bot.get_all_members():
        print(member)


@bot.command(name='addTally',
                description="Adds a tally",
                brief="git roasted",
                aliases=['tally', 'addtally', 'Addtally'],
                pass_context=True)
async def addTally(ctx, desUser: str, num: int):
    if desUser in tallydict:
        tallydict[desUser] += num
        msg = desUser + ' now has ' + str(tallydict[desUser]) + ' tallies.'
        await ctx.send(msg)
    else:
        tallydict[desUser] = num
        await ctx.send(desUser + ' has recieved their first tally. They now have ' + str(tallydict[desUser]) + ' tallies.')

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

