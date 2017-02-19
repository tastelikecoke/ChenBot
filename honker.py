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

class Honker:
    """ command holder """

    def __init__(self, server):
        self.server = server
        self.data = {}
        self.prefix = "!chen "
        self.client = None

    def load(self):
        """ loads data """

        all_data = None
        with open("data/data.json", "r") as data_file:
            all_data = json.loads(data_file.read())
        try:
            self.data = all_data[self.server.id]
            self.prefix = self.data["prefix"]

        except KeyError:
            all_data[self.server.id] = {"prefix": "!chen "}
            with open("data.json", "w") as data_file:
                data_file.write(json.dumps(all_data))

    def bind_client(self, client):
        """ binds client """
        self.client = client

    async def ask(self, message):
        """ asks a command """

        chen_command = ""
        matcher = re.match(self.prefix + r"(.+)", message.content)
        if matcher:
            chen_command = matcher.group(1)

        if chen_command.startswith("help"):
            commands = [
                "Commands are:",
                '**{prefix}help** this command',
                '**{prefix}honk** honk',
                '**{prefix}meme** meme',
                '**{prefix}roll** roll dice',

                '**{prefix}resistance help** for the resistance game',
                '**{prefix}lex help** for the lexicant game',
                '**{prefix}stalk** to learn about users',
                '**{prefix}remember** to learn about users',
                '**{prefix}lang** to switch languages',
                '**{prefix}pat** pat chen',
                '**{prefix}sing** let chen sing',
                '**{prefix}critique** critique arts',
                '**{prefix}prompt** drawing prompts',
                '**{prefix}score** store scores',
            ]
            output = '\n'.join(commands).replace('{prefix}', self.prefix)
            await self.client.send_message(message.channel, output)

        if chen_command.startswith("honk"):
            rand_duration = random.randint(6, 20)
            await self.client.send_message(message.channel, "honk")
            await asyncio.sleep(rand_duration//2)
            await self.client.send_message(message.channel, "Honk")
            await asyncio.sleep(rand_duration)
            await self.client.send_message(message.channel, "HONK")

        elif chen_command.startswith("meme"):
            await self.client.send_message(message.channel, "Don't let your dreams be memes")

        elif chen_command.startswith("roll"):
            matcher = re.match(r"roll (\d+)", chen_command)
            if matcher:
                await self.client.send_message(message.channel,\
                    "You get {0}.".format(
                        random.randint(1, int(matcher.group(1)))))

        elif chen_command.startswith("die"):
            if message.author.name == "tastelikenyan":
                await self.client.send_message(message.channel, "brb going to Gensokyo")
                await self.client.logout()
                sys.exit()
            await self.client.send_message(message.channel, "no")

        elif chen_command.startswith("pat"):
            await self.client.send_message(message.channel,\
                "http://vignette4.wikia.nocookie.net/touhouanime/images/3/34/1BdaF.jpg")

        elif chen_command.startswith("critique"):
            await self.client.send_message(message.channel, random.choice([
                "try fixing the anatomy",
                "study more references",
                "there's a bit of a issue about the hands",
                "the pose is a bit awkward",
                "add more eggplants",
                "make the pose more dynamic",
                "the shading can be improved"
            ]))

        elif chen_command.startswith("prompt"):
            if chen_command.startswith("prompt daily"):
                today_random = random.Random(str(datetime.date()))
            else:
                today_random = random
            hairness = today_random.choice([
                "white-haired",
                "blonde",
                "black-haired",
                "redhead",
                "green-haired",
                "blue-haired"
            ])
            age = today_random.choice([
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
            typing = today_random.choice([
                "woman", "woman", "woman", "woman", "woman", "woman",
                "trap",
                "man", "man", "man"
            ])
            action = today_random.choice([
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
            await self.client.send_message(
                message.channel,
                "{0} {1} year old {2} {3}".format(hairness, age, typing, action)
            )




# from drunk import Drunk
# from resistance import Resistance
# from lexicant import Lexicant
# from charade import Charade

        # elif chen_command.startswith("sing"):
        #     matcher = re.match(r"sing (\w+) (\w+)", chen_command)
        #     if matcher:
        #         await self.client.send_message(message.channel,\
        #             Drunk().markov(random.randint(10, 20), matcher.group(1), matcher.group(2)))
        #     else:
        #         await client.send_message(message.channel,\
        #             Drunk().markov(random.randint(10, 20)))
    # async def askCharade(self, message):
    #     chenCommand = ""
    #     matcher = re.match(self.prefix + r"(.+)", message.content)
    #     if matcher:
    #         chenCommand = matcher.group(1)
        
    #     if chenCommand.startswith("charades"):
    #         await stores.charade.begin(message.author, message.channel)
        
    #     if stores.charade.state == "game":
    #         await stores.charade.guess(str.lower(message.content), message.author)

    # async def askResistance(self, message):
    #     chenCommand = ""
    #     matcher = re.match(stores.prefix + r"(.+)", message.content)
    #     if matcher:
    #         chenCommand = matcher.group(1)

    #     if chenCommand.startswith("resistance help"):
    #         commands = [
    #             "resistance commands are:"
    #             "**{prefix}start game**",
    #             "**{prefix}assign**",
    #             "**{prefix}yes**",
    #             "**{prefix}no**",
    #             "**{prefix}success**",
    #             "**{prefix}fail**",
    #             "use {0} start game to start playing resistance!".format(stores.prefix)
    #         ]
    #         output = '\n'.join(commands).replace('{prefix}', stores.prefix)
    #         await client.send_message(message.channel, output)

    #     if chenCommand.startswith("start game"):
    #         await stores.resistance.begin(message.mentions, message.channel)
    #     if chenCommand.startswith("assign"):
    #         await stores.resistance.beginVote(message.author, message.mentions)
    #     if chenCommand.startswith("yes"):
    #         await stores.resistance.yesVote(message.author)
    #     if chenCommand.startswith("no"):
    #         await stores.resistance.noVote(message.author)
    #     if chenCommand.startswith("success"):
    #         await stores.resistance.passMission(message.author)
    #     if chenCommand.startswith("fail"):
    #         await stores.resistance.failMission(message.author)

    # async def askLexicant(self, message):
    #     chenCommand = ""
    #     matcher = re.match(stores.prefix + r"(.+)", message.content)
    #     if matcher:
    #         chenCommand = matcher.group(1)

    #     if chenCommand.startswith("lex help"):
    #         await client.send_message(message.channel,\
    #             "commands are:\n**{0}lex help**\n**{0}lex start**\n**{0}lex**\n**{0}lex sirit**".format(
    #                 stores.prefix))
    
    #     elif chenCommand.startswith("lex start"):
    #         matcher = re.match(r"lex start (.+)", chenCommand)
    #         if matcher:
    #             await stores.lexicant.begin(matcher.group(1), message.channel)

    #     elif chenCommand.startswith("lex"):
    #         matcher = re.match(r"lex (.+)", chenCommand)
    #         if matcher:
    #             await stores.lexicant.append(matcher.group(1))

    #     if chenCommand.startswith("lex sirit"):
    #         await stores.lexicant.seerit()


    # async def ask(self, message):
    #     chenCommand = ""
    #     matcher = re.match(stores.prefix + r"(.+)", message.content)
    #     if matcher:
    #         chenCommand = matcher.group(1)


    #     elif chenCommand.startswith("stalk"):
    #         matcher = re.match(r"stalk (.+)", chenCommand)
    #         if matcher:
    #             searchkey = matcher.group(1)
    #             if searchkey in stores.asData:
    #                 await client.send_message(message.channel, stores.asData[searchkey])
    #             else:
    #                 closests = difflib.get_close_matches(searchkey, stores.asData.keys())
    #                 if len(closests) > 0:
    #                     await client.send_message(message.channel,\
    #                         "closest match: "+closests[0]+"\n"+stores.asData[closests[0]])
    #                 else:
    #                     await client.send_message(message.channel, "Can't find honk")
    #         else:
    #             await client.send_message(message.channel,\
    #                 "Invalid command. How to use: e.g. !chen stalk username")
        
    #     elif chenCommand.startswith("remember"):
    #         matcher = re.match(r"remember ([^ ]+) (.+)", chenCommand)
    #         if matcher:
    #             searchkey = matcher.group(1)
    #             searchdata = matcher.group(2)
    #             stores.asData[searchkey] = searchdata
    #             stores.store()
    #             await client.send_message(message.channel, "{0} successfully remembered".format(searchkey))
    #         else:
    #             await client.send_message(message.channel,\
    #                 "Invalid command. How to use: e.g. !chen remember username <links>")
