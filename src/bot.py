import sys
import random
import argparse
import pymongo
import discord
import re
import datetime

def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-mh', '--mongohost', type=str,
            help='The MongoDB hostname to use.', required=True, action="store")
    parser.add_argument('-mp', '--mongoport', type=int,
            help='The MongoDB port to use.', required=True, action="store")
    parser.add_argument('-d', '--dbname', type=str,
            help='The MongoDB collection to use.', required=True, action="store")
    parser.add_argument('-t', '--token', type=str,
            help='The discord token to use.', required=True, action="store")
    parser.add_argument('-g', '--guild', type=str,
            help='The discord guild to use.', required=True, action="store")
    parser.add_argument('-qc', '--quotechannel', type=int,
            help='The quotes channel to use.', required=True, action="store")
    parser.add_argument('-lc', '--leavechannel', type=int,
            help='The leave channel to use.', required=True, action="store")

    args = parser.parse_args()
    return args


def buildQuote(quoteData):
    return f'```\n{quoteData["quote"]}\n```{quoteData["user"]}'

def getQuote(user):
    name = f'<@!{user.mention[2:]}'
    quoteList = quotes.find({"user" : name})
    return random.choice([x for x in quoteList])['quote'].strip('"')

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])

    # Create database
    try:
        mongodb = pymongo.MongoClient(args.mongohost, args.mongoport)
    except pymongo.errors.ConnectionFailure as e:
        print(e)
        exit(1)

    db = mongodb[args.dbname]
    quotes = db.quotes

    # Setup discord
    intents = discord.Intents(messages=True, guilds=True, members=True)
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == args.guild:
                break

        print(
                f'{client.user} has connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
        )
            
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        userRegex = r'<@!([0-9])*>'
        quoteRegex = r'".*"'

        commands = {
                "quoteadd" : r'super hans add quote <@!([0-9])*> ".*"',
                "help" : r'super hans help me',
                "randomquote" : r'super hans random quote <@!([0-9])*>'
        }
        
        if re.search(commands["help"], message.content) != None:
            quote = getQuote(client.user)
            helpMessage = f'{quote}```super hans add quote @user "quote"\nsuper hans random quote @user```'
            await message.channel.send(helpMessage)

        elif re.search(commands["quoteadd"], message.content) != None:
            print(f"Received quoteadd request: {message.content}")
            user = re.search(userRegex, message.content).group()
            quote = re.search(quoteRegex, message.content).group()
            time = datetime.datetime.now()

            quoteData = {
                "time" : str(time),
                "user" : user,
                "quote" : quote
            }
            print(f"Inserting {quoteData}")
            quotes.insert_one(quoteData)

            response = f'Tell you what, those quotes are really moreish'
            await message.channel.send(response)
            await message.delete()
            channel = client.get_channel(args.quotechannel)
            await channel.send(buildQuote(quoteData))

        elif re.search(commands["randomquote"], message.content) != None:
            print(f"Received randomquote request: {message.content}")
            user = re.search(userRegex, message.content)
            results = quotes.find({"user" : user.group()})
            resultsList = [x for x in results]
            if resultsList != []:
                userQuote = random.choice(resultsList)
                print(f"Found {userQuote}")
                await message.channel.send(buildQuote(userQuote))
            else:
                await message.channel.send("Couldn't find any quotes!")

    @client.event
    async def on_member_remove(user):
        channel = client.get_channel(args.leavechannel)
        quote = getQuote(client.user)
        await channel.send(f"<@{user.id}> left! {quote}")

    # Run discord bot
    client.run(args.token)
