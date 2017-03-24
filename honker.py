import asyncio
import random
import json
import string
import sys
import re
import difflib
import datetime
import urllib
from PIL import Image, ImageFont, ImageDraw
from mods import lexicant, eroge

class Honker:
    """ command holder """

    def __init__(self, server):
        self.server = server
        self.data = {}
        self.prefix = "!chen "
        self.client = None
        self.lexicant = lexicant.Lexicant(None)
        self.eroge = eroge.Eroge(None)
        self.status_report = ""
        self.dailies = []
        self.current_done_day = ""
        self.greet_channel = None

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
            with open("data/data.json", "w") as data_file:
                data_file.write(json.dumps(all_data))

    def save_only(self):
        """ save data """

        all_data = {}
        with open("data/data.json", "r") as data_file:
            all_data = json.loads(data_file.read())

        all_data[self.server.id] = self.data

        with open("data/data.json", "w") as data_file:
            data_file.write(json.dumps(all_data))

    def bind_client(self, client):
        """ binds client """
        self.client = client
        self.lexicant.sendMessageFunc = self.client.send_message
        self.eroge.sendMessageFunc = self.client.send_message

    async def clock(self):
        channel = self.greet_channel
        if channel is None:
            return
        self.status_report += "chronic cough began\n"
        now = datetime.datetime.now()
        current_day = now.strftime("%m-%d")
        if self.current_done_day != current_day:
            # new day has begun
            self.current_done_day = current_day

            if current_day in self.data["birthday"]:
                celebrant = self.data["birthday"][current_day]
                await self.client.send_message(channel,
                    "🎊 Happy birthday {0} 🎆".format(celebrant))
                self.status_report += "{0}: {1} was greeted\n".format(now, celebrant)
            else:
                self.dailies = []
                self.status_report += "{0}: dailies was cleared\n".format(now)
        else:
            self.status_report += "{0}: nothing\n".format(now)

        if len(self.status_report) > 9000:
            print(self.status_report)
            sys.stdout.flush()
            self.status_report = self.status_report[5000:]

    def change_currency(self, shem, shemful_user, currency, function):
        if shem not in self.data:
            self.data[shem] = {}
        if shemful_user not in self.data[shem]:
            self.data[shem][shemful_user] = {}
        if currency not in self.data[shem][shemful_user]:
            self.data[shem][shemful_user][currency] = 0
        self.data[shem][shemful_user][currency] = function(self.data[shem][shemful_user][currency])
        return self.data[shem][shemful_user][currency]

    async def ask(self, message):
        """ asks a command """
        if message.author.name.startswith("Nadeko"):
            if len(message.embeds) >= 1:
                embed = str(message.embeds)

                # matcher = re.match(r".*has.*", embed)
                # if matcher:
                #     await self.client.send_message(message.channel, "mats")
                shemful_user = ""
                matcher1 = re.match(r".*Winner.*.*\*\*(\w+\#\d+)\*\*", embed)
                matcher2 = re.match(r".*\*\*(\w+\#\d+)\*\*.*winner.*", embed)
                if matcher1:
                    shemful_user = matcher1.group(1)
                if matcher2:
                    shemful_user = matcher2.group(1)
                
                if shemful_user != "":
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x+100)
                    self.save_only()
                    await self.client.send_message(message.channel,\
                        "{0} now has {1:.1f} shem coins".format(shemful_user, coins))


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
                '**{prefix}pomf** pomf',
                '**{prefix}daily** daily coins',
                '**{prefix}gacha** maybe a UR?',
                '**{prefix}roll <number>** roll a number',
                '**{prefix}pat** pat chen',
                '**{prefix}critique** critique arts',
                '**{prefix}prompt** drawing prompts',
                '**{prefix}prefix \"<prefix>\"** change prefix',
                '**{prefix}stalk <user>** to learn about users',
                '**{prefix}keep <user> <data>** to keep data about users',
                '**{prefix}rem <MM-DD> <greeting>** remember a birthday',
                '**{prefix}lex help** for the lexicant game',
                ' ',
                '**UNAVAILABLE**',
                '**{prefix}resistance help** for the resistance game',
            ]
            output = '\n'.join(commands).replace('{prefix}', self.prefix)
            await self.client.send_message(message.channel, output)

        if chen_command.startswith("rem"):
            if "birthday" not in self.data:
                self.data["birthday"] = {}
            matcher = re.match(r"rem ([0-9\-]+) ([\w\W]+)", chen_command)
            if matcher:
                date = matcher.group(1)
                celebrant = matcher.group(2)
                self.data["birthday"][date] = celebrant
                self.save_only()
                await self.client.send_message(message.channel,\
                    "{0} got it".format(date))
            else:
                await self.client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen rem <date> <links>")

        if chen_command.startswith("whisper"):
            if message.author.name == "tastelikenyan":
                await self.client.send_message(message.author, "status:\n" + self.status_report)
                self.status_report = ""
            self.greet_channel = message.channel

        if chen_command.startswith("honk"):
            rand_duration = random.randint(6, 20)
            await self.client.send_message(message.channel, "honk")
            await asyncio.sleep(rand_duration//2)
            await self.client.send_message(message.channel, "Honk")
            await asyncio.sleep(rand_duration)
            await self.client.send_message(message.channel, "HONK")

        elif chen_command.startswith("meme"):
            await self.client.send_message(message.channel, "Don't let your dreams be memes")

        elif chen_command.startswith("pomf"):
            pomf_image = Image.open("temp/honk.jpg")
            pomf_draw = ImageDraw.Draw(pomf_image)
            font = ImageFont.truetype("temp/wild.ttf", 16)
            pomf_draw.text((254, 165), message.author.name, (0, 0, 0), font=font)
            pomf_image.save('temp/honk_mod.jpg')
            with open('temp/honk_mod.jpg', 'rb') as f:
                await self.client.send_file(message.channel, f)

        elif chen_command.startswith("roll"):
            matcher = re.match(r"roll (\d+)", chen_command)
            if matcher:
                await self.client.send_message(message.channel,\
                    "You get {0}.".format(
                        random.randint(1, int(matcher.group(1)))))
        
        elif chen_command.startswith("daily"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            coins = 0
            coindelta = 10
            chimes = self.change_currency("shem", shemful_user, "chime", lambda x: x)

            msg = ""
            if shemful_user not in self.dailies:
                if random.randint(0, 5) == 0:
                    coindelta = 60
                    msg = "Lucky! "
                coindelta = int(coindelta * (1 + chimes/10.0))
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x+coindelta)
                self.save_only()
                await self.client.send_message(message.channel,\
                    "{0}{1} now has {2:.1f} shem coins".format(msg, shemful_user, coins))
                self.dailies.append(shemful_user)
            else:
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                await self.client.send_message(message.channel,\
                    "You already claimed! {0} has {1:.1f} shem coins.".format(shemful_user, coins))

        elif chen_command.startswith("gacha"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            if chen_command.startswith("gacha 100"):
                getted = random.choice(["kokeshi", "chime"])
                if getted == "kokeshi":
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-100)
                    kokeshis = self.change_currency("shem", shemful_user, "kokeshi", lambda x: x+1)
                    self.save_only()
                    await self.client.send_message(message.channel,\
                        "Gacha! You got kokeshi (🎎)! kokeshi does nothing.")
                    await self.client.send_message(message.channel,\
                        "You now have {0} 🎎!\n{1} has {2:.1f} shem coins.".format(kokeshis, shemful_user, coins))

                
                if getted == "chime":
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-100)
                    chimes = self.change_currency("shem", shemful_user, "chime", lambda x: x+1)
                    self.save_only()
                    await self.client.send_message(message.channel,\
                        "Gacha! You got chime (🎐)! Each chime increases coin generation by 1%.")
                    await self.client.send_message(message.channel,\
                        "You now have {0} 🎐!\n{1} has {2:.1f} shem coins.".format(chimes, shemful_user, coins))
            else:
                await self.client.send_message(message.channel,\
                    "type '{0} gacha 100' to roll! uses up 100 coins.".format(self.prefix))
                await self.client.send_message(message.channel,\
                    "type '{0} inventory' to check your inventory.".format(self.prefix))

        elif chen_command.startswith("inventory"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            string_out = ""
            coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
            if coins != 0:
                string_out += "{0} coins\n".format(coins)
            
            kokeshis = self.change_currency("shem", shemful_user, "kokeshi", lambda x: x)
            if kokeshis != 0:
                string_out += "{0} 🎎\n".format(kokeshis)
            
            chimes = self.change_currency("shem", shemful_user, "chime", lambda x: x)
            if chimes != 0:
                string_out += "{0} 🎐\n".format(chimes)
            
            await self.client.send_message(message.channel, string_out)

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

        elif chen_command.startswith("prefix"):
            matcher = re.match(r"prefix \"(.+)\"", chen_command)
            if matcher:
                self.prefix = matcher.group(1)
                self.data["prefix"] = self.prefix
                self.save_only()

                await self.client.send_message(message.channel,\
                    "new prefix is {0}".format(self.prefix))

        elif chen_command.startswith("stalk"):
            if "keep" not in self.data:
                self.data["keep"] = {}
            matcher = re.match(r"stalk (.+)", chen_command)
            if matcher:
                searchkey = matcher.group(1)
                if searchkey in self.data["keep"]:
                    await self.client.send_message(message.channel, self.data["keep"][searchkey])
                else:
                    closests = difflib.get_close_matches(searchkey, self.data["keep"].keys())
                    if len(closests) > 0:
                        await self.client.send_message(message.channel,\
                            "closest match: {0}:\n{1}".format(\
                                closests[0], self.data["keep"][closests[0]]))
                    else:
                        await self.client.send_message(message.channel, "Can't find honk")
            else:
                await self.client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen stalk username")

        elif chen_command.startswith("keep"):
            if "keep" not in self.data:
                self.data["keep"] = {}
            matcher = re.match(r"keep ([^ ]+) ([\w\W]+)", chen_command)
            if matcher:
                searchkey = matcher.group(1)
                searchdata = matcher.group(2)
                self.data["keep"][searchkey] = searchdata
                self.save_only()
                await self.client.send_message(message.channel,\
                    "{0} successfully remembered".format(searchkey))
            else:
                await self.client.send_message(message.channel,\
                    "Invalid command. How to use: e.g. !chen keep username <links>")

        elif chen_command.startswith("eroge"):
            await self.eroge.begin(message.channel)
        elif chen_command.startswith("eroge end"):
            await self.eroge.end()

        # lex parts
        elif chen_command.startswith("lex help"):
            await self.client.send_message(message.channel,\
                "commands are:\n**{0}lex help**\n**{0}lex start <letter>**\n**{0}lex end**\n**{0}lex sirit**".format(
                    self.prefix))
        elif chen_command.startswith("lex start"):
            matcher = re.match(r"lex start (.+)", chen_command)
            if matcher:
                await self.lexicant.begin(matcher.group(1), message.channel)
        elif chen_command.startswith("lex sirit"):
            await self.lexicant.seerit()
        elif chen_command.startswith("lex end"):
            await self.lexicant.end()

        if self.lexicant.state == "game" and message.channel == self.lexicant.channel:
            await self.lexicant.append(message.content)
        if self.eroge.state == "game" and message.channel == self.eroge.channel:
            await self.eroge.next(message.content)


# from resistance import Resistance
# from lexicant import Lexicant
# from charade import Charade

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
