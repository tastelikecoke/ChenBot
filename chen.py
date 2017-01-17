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
from drunk import Drunk
from resistance import Resistance

class Stores:
    storedChannel = None
    localization = "en"
    def accessFile(self):
        with open("voltexes.json", "r") as voltexesFile:
            self.courses = json.loads(voltexesFile.read())
        with open("secrets.json", "r") as secretsFile:
            self.secrets = json.loads(secretsFile.read())
        with open("asdata.json", "r") as asDataFile:
            self.asData = json.loads(asDataFile.read())
    def __init__(self, client):
        self.accessFile()
        self.mainCommand = MainCommand()
        self.resistance = Resistance(client.send_message)
        self.killer = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
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

class MainCommand:
    async def askResistance(self, message):
        if message.content.startswith("chen start game"):
            await stores.resistance.begin(message.mentions, message.channel)
        if message.content.startswith("chen assign"):
            await stores.resistance.beginVote(message.author, message.mentions)
        if message.content.startswith("chen yes"):
            await stores.resistance.yesVote(message.author)
        if message.content.startswith("chen no"):
            await stores.resistance.noVote(message.author)
        if message.content.startswith("chen success"):
            await stores.resistance.passMission(message.author)
        if message.content.startswith("chen fail"):
            await stores.resistance.failMission(message.author)

    async def ask(self, message):
        if message.content.startswith("chen pls honk"):
            await client.send_message(message.channel, stores.localize("honk"))
            await asyncio.sleep(10)
            await client.send_message(message.channel, stores.localize("HONK"))
        elif message.content.startswith("chen stalk"):
            matcher = re.match(r"chen stalk (.+)", message.content)
            if matcher:
                searchkey = matcher.group(1)
                if searchkey in stores.asData:
                    await client.send_message(message.channel, stores.asData[searchkey])
                else:
                    closests = difflib.get_close_matches(searchkey, stores.asData.keys())
                    if len(closests) > 0:
                        await client.send_message(message.channel, "closest match: "+closests[0]+"\n"+stores.asData[closests[0]])
                    else:
                        await client.send_message(message.channel, "Can't find that guy honk")
        elif message.content.startswith("chen english pls"):
            stores.localization = "en"
            await client.send_message(message.channel, stores.localize("roger!"))
        elif message.content.startswith("chen japanese pls"):
            stores.localization = "jp"
            await client.send_message(message.channel, stores.localize("roger!"))
        elif message.content.startswith("chen pls help"):
            commands = [
                stores.localize("Commands are:"),
                "* chen pls honk",
                "* chen pls help",
                "* chen inspire me",
                "* chen pls die",
                "* chen start game",
                "* chen roll <number>",
                "* chen pat",
                "* chen lewd",
            ]
            await client.send_message(message.channel, '\n'.join(commands))
        elif message.content.startswith("chen inspire me"):
            await client.send_message(message.channel, stores.localize("Don't let your dreams be memes"))
        elif message.content.startswith("chen roll"):
            matcher = re.match(r"chen roll (\d+)", message.content)
            if matcher:
                await client.send_message(message.channel, stores.localize("You get {0}.").format(random.randint(1, int(matcher.group(1))+1)))
        elif message.content.startswith("chen pls die"):
            if message.author.name == "tastelikenyan":
                await client.send_message(message.channel, stores.localize("brb going to Gensokyo"))
                await client.logout()
                sys.exit()
            await client.send_message(message.channel, stores.localize("no"))
        elif message.content.startswith("chen celebrate"):
            await client.send_message(message.channel, stores.localize("✨🎉🎊✨"))
        elif message.content.startswith("chen pat"):
            await client.send_message(message.channel, "http://vignette4.wikia.nocookie.net/touhouanime/images/3/34/1BdaF.jpg")
        elif message.content.startswith("chen lewd"):
            await client.send_message(message.channel, "http://orig03.deviantart.net/115a/f/2012/266/9/9/honk_by_cybeam100-d5fnxir.jpg")
        elif message.content.startswith("chen voltex"):
            await client.send_message(message.channel, "play {}".format(random.choice(stores.courses)["name"]))
        elif message.content.startswith("chen sing"):
            await client.send_message(message.channel, Drunk().markov(random.randint(10,20)))
        elif message.content.startswith("chen pls sing"):
            matcher = re.match(r"chen pls sing (\w+) (\w+)", message.content)
            if matcher:
                await client.send_message(message.channel, Drunk().markov(random.randint(10,20), matcher.group(1), matcher.group(2)))
        elif message.content.startswith("chen pls critique"):
            await client.send_message(message.channel, random.choice([
                "try fixing the anatomy",
                "study more references",
                "there's a bit of a problem in the hands",
                "the pose is a bit awkward",
            ]))


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
