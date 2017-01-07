# _*_ coding:utf-8 _*_
import discord
import asyncio
import random
import json

client = discord.Client()

voltexesFile = open("voltexes.json", "r")
courses = json.loads(voltexesFile.read())

secretsFile = open("secrets.json", "r")
secrets = json.loads(secretsFile.read())

class Stores:
    x = ""
    password = ""
    amount = 0
    votes = {}
    def store(self, a):
        self.x = a
    def get(self):
        return self.x
    def store_vote(self, user):
        if user in self.votes:
            self.votes[user] += 1
        else:
            self.votes[user] = 1
    def reset(self):
        self.votes = {}

stores = Stores()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    stores.password = random.choice(["cheeen", "cheeeeeen", "cheeeeen"])

@client.event
async def on_message(message):
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
try:
    client.run(secrets["token"])
except KeyboardInterrupt as e:
    print("Interrupted. Will die.")
    client.logout()
