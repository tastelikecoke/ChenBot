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
    channel = None
    def reset(self):
        self.players = []
        self.votes = []
        self.novotes = []
    def setPlayers(self, players):
        self.players = players
    def giveRoles(self):
        for player in self.players:
            self.roles[player] = random.choice(["good", "bad"])
        self.current = random.choice(self.players)
        self.state = "assign"
    def sayPlayers(self, players):
        output = ""
        for player in players:
            output += player.name + " - " + self.roles[player] + "\n"
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
                await client.send_message(self.channel, "mission fail.")
            else:
                await client.send_message(self.channel, "mission success.")
            await self.startAssign()
    async def startAssign(self):
        self.votes = []
        self.novotes = []
        self.state = "assign"
        self.current = random.choice(self.players)
        await client.send_message(self.channel, "new mission! " + self.current.name + " is assigning.\n use chen assign")
    async def startVote(self):
        self.votes = []
        self.novotes = []
        self.state = "vote"
        await client.send_message(self.channel, "Vote now! either chen yes or chen no")
    async def pushMission(self):
        self.votes = []
        self.novotes = []
        self.state = "mission"
        for player in self.missioned:
            if self.roles[player] == "bad":
                await client.send_message(player, "are you success? y/n")
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
            self.reset()
            self.channel = message.channel
            mentioned = message.mentions
            self.setPlayers(mentioned)
            self.giveRoles()
            for player in self.players:
                await client.send_message(player, "you are " + self.roles[player])
            await self.startAssign()
        if message.content.startswith("chen assign"):
            if self.state == "assign":
                if self.current == message.author:
                    self.missioned = message.mentions
                    for mention in message.mentions:
                        if mention not in self.players:
                            await client.send_message(message.channel, "pls, players only")
                            return
                    if len(message.mentions) <= 0:
                        await client.send_message(message.channel, "nobody is assigned. pls do it again honk")
                        return

                    await client.send_message(message.channel, "roger!")
                    await client.send_message(message.channel, "mission:\n" + self.sayPlayers(self.missioned))
                    await self.startVote()
        if message.content.startswith("chen yes"):
            if self.state == "vote":
                if self.vote(message.author):
                    await client.send_message(message.channel, "roger!")
                    if self.checkMission():
                        await client.send_message(message.channel, "mission push!")
                        await self.pushMission()
                else:
                    await client.send_message(message.channel, "no")
        if message.content.startswith("chen no"):
            if self.state == "vote":
                if self.vote(message.author):
                    await client.send_message(message.channel, "roger!")
                    if self.checkUnMission():
                        await client.send_message(message.channel, "vote failed.")
                        await self.startAssign()
                else:
                    await client.send_message(message.channel, "no")

        if message.content.startswith("chen game?"):
            await client.send_message(message.channel, "game is in " + self.state + " state.")

class MainCommand:
    async def ask(self, message):
        if message.content.startswith("chen pls honk"):
            await client.send_message(message.channel, "honk")
        elif message.content.startswith("chen pls die"):
            matcher = re.match(r"chen pls die (.+)", message.content)
            if matcher:
                if matcher.group(1) == stores.killer:
                    await client.send_message(message.channel, "brb going to Gensokyo")
                    await client.logout()
                    sys.exit()
            await client.send_message(message.channel, "no")

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
    if message.content.startswith('~test~'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith("~meme~"):
        await client.send_message(message.channel, "Ｄｏｎ’ｔ　ｌｅｔ　ｙｏｕｒ　ｄｒｅａｍｓ　ｂｅ　ｍｅｍｅｓ")
    elif message.content.startswith("~honk~"):
        if message.author != client.user:
            await client.send_message(message.channel, "ｈｏｎｋ")
            await asyncio.sleep(10)
            await client.send_message(message.channel, "ＨＯＮＫ")
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
    elif message.content.startswith("~mynameis~"):
        argument = message.content.split(" ")[1]
        stores.store(argument)
    elif message.content.startswith("~yourrope~"):
        await client.send_message(message.channel, stores.get())
    elif message.content.startswith("~players~"):
        mentioned = message.mentions
        stores.amount = len(mentioned)
        players = "Players\n"
        for player in mentioned:
            players += str(player.name) + "\n"
        await client.send_message(message.channel, players)
    elif message.content.startswith("~vote~"):
        firstmention = message.mentions[0]
        stores.store_vote(firstmention)
        votings = "Votal\n"
        islynch = None
        for vote in stores.votes:
            votings += str(vote.name) + " - " + str(stores.votes[vote]) + "\n"
            if stores.votes[vote] >= stores.amount/2:
                islynch = vote
        await client.send_message(message.channel, votings)
        if islynch is not None:
            stores.reset()
            await client.send_message(message.channel, str(vote.name)+" is lynched")
            await client.send_message(message.channel, "Next day someone died!  Chen doesn't know who")
    elif message.content.startswith("~night~"):
        stores.reset()
        await client.send_message(message.channel, "Next day someone died!  Chen doesn't know who")
    elif message.content.startswith("~roll~"):
        argument = message.content.split(" ")[1]
        await client.send_message(message.channel, "{0}".format(random.randint(1, int(argument)+1)))
    elif message.content.startswith("~count~"):
        argument = message.content.split(" ")[1]
        period = int(argument)
        counter = await client.send_message(message.channel, "counting...")
        for i in range(period):
            await asyncio.sleep(1)
            await client.edit_message(counter, str(i))
            """
