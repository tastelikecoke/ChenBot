# _*_ coding:utf-8 _*_
import discord
import asyncio
import random
import json
import string
import sys
import traceback
import re
import difflib
import urllib
import datetime
from drunk import Drunk
from resistance import Resistance
from lexicant import Lexicant
from charade import Charade

class Stores:
    storedChannel = None
    localization = "en"
    prefix = "!chen "
    def accessFile(self):
        with open("secrets.json", "r") as secretsFile:
            self.secrets = json.loads(secretsFile.read())
        with open("asdata.json", "r") as asDataFile:
            self.asData = json.loads(asDataFile.read())
        with open("scores.json", "r") as scoreDataFile:
            self.scoreData = json.loads(scoreDataFile.read())
        with open("words.txt", "r") as wordDataFile:
            self.wordData = wordDataFile.read()
    def __init__(self, client):
        self.accessFile()
        self.mainCommand = MainCommand()
        self.resistance = Resistance(client.send_message)
        self.lexicant = Lexicant(client.send_message, self.wordData)
        self.charade = Charade(client.send_message, self.wordData.split("\n"))
        self.killer = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
    def store(self):
        with open("asdata.json", "w") as asDataFile:
            asDataFile.write(json.dumps(self.asData))
        with open("scores.json", "w") as scoreDataFile:
            scoreDataFile.write(json.dumps(self.scoreData))

    def localize(self, val):
        if self.localization == "jp":
            if val == "Don't let your dreams be memes":
                return "ミームを夢になれなきゃ"
            if val == "honk":
                return "パフ"
            if val == "HONK":
                return "パーーフ"
            if val == "roger!":
                return "ようかい！"
            if val == "no":
                return "ノー"
            if val == "You get {0}.":
                return "{0}をもらう"
            if val == "brb going to Gensokyo":
                return "死にます！さよなら"
        return val
    async def ask(self, message):
        await self.mainCommand.ask(message)
        await self.mainCommand.askResistance(message)
        await self.mainCommand.askCharade(message)
        await self.mainCommand.askLexicant(message)

class MainCommand:
    async def askCharade(self, message):
        chenCommand = ""
        matcher = re.match(stores.prefix + r"(.+)", message.content)
        if matcher:
            chenCommand = matcher.group(1)
        
        if chenCommand.startswith("charades"):
            await stores.charade.begin(message.author, message.channel)
        
        if stores.charade.state == "game":
            await stores.charade.guess(str.lower(message.content), message.author)

    async def askResistance(self, message):
        chenCommand = ""
        matcher = re.match(stores.prefix + r"(.+)", message.content)
        if matcher:
            chenCommand = matcher.group(1)

        if chenCommand.startswith("resistance help"):
            commands = [
                "resistance commands are:"
                "**{prefix}start game**",
                "**{prefix}assign**",
                "**{prefix}yes**",
                "**{prefix}no**",
                "**{prefix}success**",
                "**{prefix}fail**",
                "use {0} start game to start playing resistance!".format(stores.prefix)
            ]
            output = '\n'.join(commands).replace('{prefix}', stores.prefix)
            await client.send_message(message.channel, output)

        if chenCommand.startswith("start game"):
            await stores.resistance.begin(message.mentions, message.channel)
        if chenCommand.startswith("assign"):
            await stores.resistance.beginVote(message.author, message.mentions)
        if chenCommand.startswith("yes"):
            await stores.resistance.yesVote(message.author)
        if chenCommand.startswith("no"):
            await stores.resistance.noVote(message.author)
        if chenCommand.startswith("success"):
            await stores.resistance.passMission(message.author)
        if chenCommand.startswith("fail"):
            await stores.resistance.failMission(message.author)

    async def askLexicant(self, message):
        chenCommand = ""
        matcher = re.match(stores.prefix + r"(.+)", message.content)
        if matcher:
            chenCommand = matcher.group(1)

        if chenCommand.startswith("lex help"):
            await client.send_message(message.channel,\
                "commands are:\n**{0}lex help**\n**{0}lex start**\n**{0}lex**\n**{0}lex sirit**".format(
                    stores.prefix))
    
        elif chenCommand.startswith("lex start"):
            matcher = re.match(r"lex start (.+)", chenCommand)
            if matcher:
                await stores.lexicant.begin(matcher.group(1), message.channel)

        elif chenCommand.startswith("lex"):
            matcher = re.match(r"lex (.+)", chenCommand)
            if matcher:
                await stores.lexicant.append(matcher.group(1))

        if chenCommand.startswith("lex sirit"):
            await stores.lexicant.seerit()


    async def ask(self, message):
        chenCommand = ""
        matcher = re.match(stores.prefix + r"(.+)", message.content)
        if matcher:
            chenCommand = matcher.group(1)

        if chenCommand.startswith("help"):
            commands = [
                stores.localize("Commands are:"),
                '**{prefix}help** this command',
                '**{prefix}resistance help** for the resistance game',
                '**{prefix}lex help** for the lexicant game',
                '**{prefix}honk** honk',
                '**{prefix}stalk** to learn about users',
                '**{prefix}remember** to learn about users',
                '**{prefix}lang** to switch languages',
                '**{prefix}meme** meme',
                '**{prefix}roll** roll dice',
                '**{prefix}pat** pat chen',
                '**{prefix}sing** let chen sing',
                '**{prefix}critique** critique arts',
                '**{prefix}prompt** drawing prompts',
                '**{prefix}score** store scores',
            ]
            output = '\n'.join(commands).replace('{prefix}', stores.prefix)
            await client.send_message(message.channel, output)

        elif chenCommand.startswith("honk"):
            await client.send_message(message.channel, stores.localize("honk"))
            await asyncio.sleep(10)
            await client.send_message(message.channel, stores.localize("HONK"))

        elif chenCommand.startswith("stalk"):
            matcher = re.match(r"stalk (.+)", chenCommand)
            if matcher:
                searchkey = matcher.group(1)
                if searchkey in stores.asData:
                    await client.send_message(message.channel, stores.asData[searchkey])
                else:
                    closests = difflib.get_close_matches(searchkey, stores.asData.keys())
                    if len(closests) > 0:
                        await client.send_message(message.channel,\
                            "closest match: "+closests[0]+"\n"+stores.asData[closests[0]])
                    else:
                        await client.send_message(message.channel, "Can't find honk")
            else:
                await client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen stalk username")
        
        elif chenCommand.startswith("remember"):
            matcher = re.match(r"remember ([^ ]+) (.+)", chenCommand)
            if matcher:
                searchkey = matcher.group(1)
                searchdata = matcher.group(2)
                stores.asData[searchkey] = searchdata
                stores.store()
                await client.send_message(message.channel, "{0} successfully remembered".format(searchkey))
            else:
                await client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen remember username <links>")

        elif chenCommand.startswith("lang"):
            matcher = re.match(r"lang (.+)", chenCommand)
            if matcher:
                stores.localization = matcher.group(1)
                await client.send_message(message.channel, stores.localize("roger!"))
            else:
                await client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen lang jp")

        elif chenCommand.startswith("meme"):
            await client.send_message(message.channel,\
                stores.localize("Don't let your dreams be memes"))

        elif chenCommand.startswith("roll"):
            matcher = re.match(r"roll (\d+)", chenCommand)
            if matcher:
                await client.send_message(message.channel,\
                    stores.localize("You get {0}.").format(
                        random.randint(1, int(matcher.group(1)))))

        elif chenCommand.startswith("die"):
            if message.author.name == "tastelikenyan":
                await client.send_message(message.channel, stores.localize("brb going to Gensokyo"))
                await client.logout()
                sys.exit()
            await client.send_message(message.channel, stores.localize("no"))

        elif chenCommand.startswith("pat"):
            await client.send_message(message.channel,\
                "http://vignette4.wikia.nocookie.net/touhouanime/images/3/34/1BdaF.jpg")

        elif chenCommand.startswith("sing"):
            matcher = re.match(r"sing (\w+) (\w+)", chenCommand)
            if matcher:
                await client.send_message(message.channel,\
                    Drunk().markov(random.randint(10, 20), matcher.group(1), matcher.group(2)))
            else:
                await client.send_message(message.channel,\
                    Drunk().markov(random.randint(10, 20)))

        elif chenCommand.startswith("critique"):
            await client.send_message(message.channel, random.choice([
                "try fixing the anatomy",
                "study more references",
                "there's a bit of a issue about the hands",
                "the pose is a bit awkward",
                "add more eggplants",
                "make the pose more dynamic",
                "the shading can be improved"
            ]))

        elif chenCommand.startswith("prompt"):
            if chenCommand.startswith("prompt daily"):
                todayRandom = random.Random(str(datetime.date))
            else:
                todayRandom = random

            hairness = todayRandom.choice([
                "white-haired",
                "blonde",
                "black-haired",
                "redhead",
                "green-haired",
                "blue-haired"
            ])
            age = todayRandom.choice([
                "9",
                "13",
                "16", "16",
                "18", "18", "18", "18",
                "20", "20", "20", "20", "20",
                "21", "21", "21", "21",
                "25", "25", "25",
                "29", "29",
                "33",
                "40",
                "50",
                "70"
            ])
            typing = todayRandom.choice([
                "woman", "woman", "woman", "woman", "woman", "woman",
                "trap",
                "man", "man", "man"
            ])
            action = todayRandom.choice([
                "reading a book",
                "smiling",
                "smiling",
                "posing for camera",
                "swimming",
                "walking the dog",
                "thinking about life",
                "standing",
                "sitting",
                "doing a selfie"
            ])
            await client.send_message(message.channel, "{0} {1} year old {2} {3}".format(hairness, age, typing, action))
        
        elif chenCommand.startswith("score"):
            matcher = re.match(r"score ([0-9]+) (.+)", chenCommand)
            if matcher:
                score = int(matcher.group(1))
                song = matcher.group(2)
                if song not in stores.scoreData:
                    stores.scoreData[song] = {}
                stores.scoreData[song][message.author.name] = score
                stores.store()
                await client.send_message(message.channel, "{0}'s score of {1} in {2} stored.".format(message.author.name, score, song))
                return
            matcher = re.match(r"score (.+)", chenCommand)
            if matcher:
                song = matcher.group(1)
                if song in stores.scoreData:
                    output = ""
                    scores = stores.scoreData[song]
                    for scorer in scores:
                        output = "{0}: {1}".format(scorer, scores[scorer])
                    await client.send_message(message.channel, output)
                else:
                    await client.send_message(message.channel, "no scores honk.")
                return

client = discord.Client()
stores = Stores(client)

@client.event
async def on_ready():
    print('Logged in as {0}'.format(client.user.name))
    sys.stdout.flush()

@client.event
async def on_message(message):
    try:
        await stores.ask(message)
    except Exception as e:
        print("Fix this bug:{}".format(e))
        traceback.print_exc()

client.run(stores.secrets["token"])
