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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('ｔｅｓｔ'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('ｓｌｅｅｐ'):
        await asyncio.sleep(60)
        await client.send_message(message.channel, 'Ｄｏｎｅ　ｓｌｅｅｐｉｎｇ')
    elif message.content.startswith("ｍｅｍｅ"):
        await client.send_message(message.channel, "Ｄｏｎ’ｔ　ｌｅｔ　ｙｏｕｒ　ｄｒｅａｍｓ　ｂｅ　ｍｅｍｅｓ")
    elif message.content.startswith("ｈｏｎｋ"):
        if message.author != client.user:
            await client.send_message(message.channel, "ｈｏｎｋ")
    elif message.content.startswith("!help"):
        await client.send_message(message.channel, "Commands are: ｔｅｓｔ, ｓｌｅｅｐ, ｍｅｍｅ, ｈｏｎｋ, ｈｅｌｐ")
        await client.send_message(message.channel, "Please don't bully me")
    elif message.content.startswith("!die"):
        await client.logout()
    elif message.content.startswith("!aesthetic"):
        argument = message.content.split(" ")[1]
        argumentwide = "".join([alphabet[ord(x) - ord('a')] for x in argument])
        await client.send_message(message.channel, argumentwide)
    elif message.content.startswith("!voltex"):
        await client.send_message(message.channel, "play " + random.choice(courses)["name"])
try:
    client.run(secrets["token"])
except KeyboardInterrupt as e:
    print("Interrupted. Will die.")
    client.logout()
