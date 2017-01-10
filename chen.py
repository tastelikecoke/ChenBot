# _*_ coding:utf-8 _*_
import discord
import asyncio
import random
import json
import string
import sys
import traceback
import re

class Stores:
    listeners = []
    localization = "en"
    def accessFile(self):
        with open("voltexes.json", "r") as voltexesFile:
            self.courses = json.loads(voltexesFile.read())
        with open("secrets.json", "r") as secretsFile:
            self.secrets = json.loads(secretsFile.read())
    def __init__(self):
        self.accessFile()
        self.mainCommand = MainCommand()
        self.resistance = Resistance()
        self.killer = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
    def localize(self, string):
        if self.localization == "jp":
            if string == "Don't let your dreams be memes":
                return "ミームを夢になれなきゃ"
            if string == "honk":
                return "パフ"
            if string == "HONK":
                return "パーーフ"
            if string == "roger!":
                return "ようかい！"
            if string == "no":
                return "ノー"
            if string == "You get {0}.":
                return "{0}をもらう"
            if string == "brb going to Gensokyo":
                return "死にます！さよなら"
        return string
    def listen(self, user, yes, no, func):
        async def isYes(message):
            if message.author == user:
                if message.content == yes:
                    await func(True)
                    return True
                elif message.content == no:
                    await func(False)
                    return True
        self.listeners.append(isYes)
    async def ask(self, message):
        await self.mainCommand.ask(message)
        await self.resistance.ask(message)
        listeners_new = []
        for listener in self.listeners:
            answer = await listener(message)
            if not answer:
                listeners_new.append(listener)
        self.listeners = listeners_new
class Resistance:
    players = []
    roles = {}
    missioned = []
    state = "" # vote -> missioning -> vote
    votes = []
    novotes = []
    current = None
    currentIdx = 0
    channel = None
    missioneers = [0.3, 0.5, 0.7, 0.1]
    missionIndex = 0
    failPoints = 0
    successPoints = 0
    def setPlayers(self, players):
        self.players = players
        self.votes = []
        self.novotes = []
        self.missionIndex = 0
    def giveRoles(self):
        for player in self.players:
            self.roles[player] = random.choice(["resistance", "spy"])
        self.currentIdx = random.randint(0, len(self.players))
        self.state = "assign"
    def sayPlayers(self, players):
        output = ""
        for player in players:
            output += player.name + "\n"
        return output
    def vote(self, voter):
        if voter in self.players and voter not in self.votes:
            self.votes.append(voter)
            return True
        else:
            return False
    def checkMission(self):
        return len(self.votes) > len(self.players)/2
    def checkUnMission(self):
        if len(self.players) % 2 == 0:
            return len(self.votes) >= len(self.players)/2
        return len(self.votes) > len(self.players)/2
    def missioneerReq(self):
        req = int(self.missioneers[self.missionIndex]*float(len(self.players)))
        if req == 0:
            return 1
        return req
    async def doMission(self, doer):
        if doer in self.missioned:
            self.votes.append(doer)
        await self.checkSuccess(doer)
    async def failMission(self, doer):
        if doer in self.missioned:
            self.novotes.append(doer)
        await self.checkSuccess(doer)
    async def checkSuccess(self, doer):
        if len(self.votes) + len(self.novotes) >= len(self.missioned):
            if len(self.novotes) > 0:
                await client.send_message(self.channel, "Mission Fail.")
                await client.send_message(self.channel, "fails: {0}, success: {1}".format(self.failPoints, self.successPoints))
                self.failPoints += 1
            else:
                await client.send_message(self.channel, "Mission Success!")
                self.successPoints += 1
            self.missionIndex += 1
            await client.send_message(self.channel, "fails: {0}, success: {1}".format(self.failPoints, self.successPoints))
            if self.missionIndex >= len(self.missioneers):
                await client.send_message(self.channel, "Game End.")
                self.missionIndex = 0
            else:
                await self.startAssign()
    async def startAssign(self):
        self.votes = []
        self.novotes = []
        self.state = "assign"
        self.current = self.players[self.currentIdx]
        self.currentIdx = (self.currentIdx + 1) % len(self.players)
        await client.send_message(self.channel, "Mission {0}\n".format(self.missionIndex+1) + self.current.name + " is assigning.\n use chen assign")
        await client.send_message(self.channel, "you need to assign {0}".format(self.missioneerReq()))
    async def startVote(self):
        self.votes = []
        self.novotes = []
        self.state = "vote"
        await client.send_message(self.channel, "Vote now! to vote: either say chen yes or chen no")
    async def pushMission(self):
        self.votes = []
        self.novotes = []
        self.state = "mission"
        for player in self.missioned:
            if self.roles[player] == "spy":
                await client.send_message(player, "are you success? say either y or n")
                async def func(yesno):
                    if yesno:
                        await self.doMission(player)
                    else:
                        await self.failMission(player)
                    await client.send_message(player, "got it")
                stores.listen(player, "y", "n", func)
            else:
                await self.doMission(player)

    async def ask(self, message):
        if message.content.startswith("chen start game"):
            self.channel = message.channel
            mentioned = message.mentions
            if len(mentioned) == 0:
                await client.send_message(self.channel, "Pls mention players")
                return
            self.setPlayers(mentioned)
            self.giveRoles()
            for player in self.players:
                await client.send_message(player, "You are " + self.roles[player])
            await client.send_message(self.channel, "Players:\n" + self.sayPlayers(self.players))
            await self.startAssign()
        if message.content.startswith("chen assign"):
            if self.state == "assign":
                if self.current == message.author:
                    self.missioned = message.mentions
                    for mention in message.mentions:
                        if mention not in self.players:
                            await client.send_message(self.channel, "pls, players only")
                            return
                    if len(message.mentions) != self.missioneerReq():
                        await client.send_message(self.channel, "pls do it again honk")
                        return
                    await client.send_message(self.channel, "roger!")
                    await client.send_message(self.channel, "Mission Members:\n" + self.sayPlayers(self.missioned))
                    await self.startVote()
        if message.content.startswith("chen yes"):
            if self.state == "vote":
                if self.vote(message.author):
                    await client.send_message(self.channel, "roger!")
                    if self.checkMission():
                        await client.send_message(self.channel, "Mission Start!")
                        await self.pushMission()
                else:
                    await client.send_message(self.channel, "no")
        if message.content.startswith("chen no"):
            if self.state == "vote":
                if self.vote(message.author):
                    await client.send_message(self.channel, "roger!")
                    if self.checkUnMission():
                        await client.send_message(self.channel, "Mission Vetoed...")
                        await self.startAssign()
                else:
                    await client.send_message(self.channel, "no")
        if message.content.startswith("chen status"):
            await client.send_message(message.channel, "Resistance game is in " + self.state + " state.")

class MainCommand:
    async def ask(self, message):
        if message.content.startswith("chen pls honk"):
            await client.send_message(message.channel, stores.localize("honk"))
            await asyncio.sleep(10)
            await client.send_message(message.channel, stores.localize("HONK"))
        elif message.content.startswith("chen english pls"):
            stores.localization = "en"
            await client.send_message(message.channel, stores.localize("roger!"))
        elif message.content.startswith("chen japanese pls"):
            stores.localization = "jp"
            await client.send_message(message.channel, stores.localize("roger!"))
        elif message.content.startswith("chen pls help"):
            commands = ["* chen pls honk", "* chen pls help", "* chen inspire me", "* chen pls die", "* chen start game", "* chen roll <number>", "* chen pat", "* chen lewd"]
            await client.send_message(message.channel, stores.localize("Commands are:"))
            await client.send_message(message.channel, '\n'.join(commands))
        elif message.content.startswith("chen inspire me"):
            await client.send_message(message.channel, stores.localize("Don't let your dreams be memes"))
        elif message.content.startswith("chen roll"):
            matcher = re.match("chen roll (\d+)", message.content)
            if matcher:
                await client.send_message(message.channel, stores.localize("You get {0}.").format(random.randint(1, int(matcher.group(1))+1)))
        elif message.content.startswith("chen pls die"):
            if message.author.name == "tastelikenyan":
                await client.send_message(message.channel, stores.localize("brb going to Gensokyo"))
                await client.logout()
                sys.exit()
            await client.send_message(message.channel, stores.localize("no"))
        elif message.content.startswith("chen pat"):
            await client.send_message(message.channel, "http://vignette4.wikia.nocookie.net/touhouanime/images/3/34/1BdaF.jpg")
        elif message.content.startswith("chen lewd"):
            await client.send_message(message.channel, "http://i1.kym-cdn.com/photos/images/facebook/000/348/330/af2.png")

stores = Stores()
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0}'.format(client.user.name))
    print(stores.killer)
    sys.stdout.flush()

@client.event
async def on_message(message):
    try:
        await stores.ask(message)
    except Exception as e:
        print("Fix this bug:".format(e))
        traceback.print_exc()

client.run(stores.secrets["token"])


f = """
    elif message.content.startswith("~help~"):
        await client.send_message(message.channel, "Commands are: ~sleep~, ~meme~, ~honk~, ~help~, ~voltex~")
        await client.send_message(message.channel, "Please don't bully me")
    elif message.content.startswith("~die~"):
        await client.send_message(message.channel, "Brb going to Gensokyo!")
        await client.logout()
    elif message.content.startswith("~aesthetic~"):
        argument = message.content.split(" ")[1]
        alphabet = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
        argumentwide = "".join([alphabet[ord(x) - ord('a')] for x in argument])
        await client.send_message(message.channel, argumentwide)
    elif message.content.startswith("~voltex~"):
        await client.send_message(message.channel, "play " + random.choice(courses)["name"])
    elif message.content.startswith("~aesthetic~"):
        argument = message.content.split(" ")[1]
        alphabet = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
        argumentwide = "".join([alphabet[ord(x) - ord('a')] for x in argument])
        await client.send_message(message.channel, argumentwide)
    elif message.content.startswith("~pat~"):
        await client.send_message(message.channel, "http://vignette4.wikia.nocookie.net/touhouanime/images/3/34/1BdaF.jpg")
    elif message.content.startswith("~lewd~"):
        await client.send_message(message.channel, "http://i1.kym-cdn.com/photos/images/facebook/000/348/330/af2.png")
            """
