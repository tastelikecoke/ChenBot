import asyncio
import random
import json
import string
import sys
import pytz
import re
import difflib
import datetime
import operator
import urllib
import math
from PIL import Image, ImageFont, ImageDraw
from mods import lexicant, eroge, hangman

class Honker:
    """ command holder """

    def __init__(self, server):
        self.server = server
        self.data = {}
        self.prefix = "!chen "
        self.client = None
        self.lexicant = lexicant.Lexicant(None)
        self.eroge = eroge.Eroge(None)
        self.hangman = hangman.Hangman(None)
        self.status_report = ""
        self.dailies = []
        self.current_done_day = ""
        self.greet_channel = None
        self.police_channel = None
        self.restricted_channel = None

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
        self.hangman.sendMessageFunc = lambda x, y: self.client.send_message(x, embed=y)
        self.hangman.addCoinsFunc = self.addCoinsFunc

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
                self.status_report += "{0}: dailies was cleared\n".format(now)
            
            self.dailies = []
        else:
            self.status_report += "{0}: nothing\n".format(now)

        if len(self.status_report) > 9000:
            self.status_report = self.status_report[5000:]

    async def addCoinsFunc(self, channel, shemful_user, cointype="coin", emoji="coin", amount=500, flavor=""):
        if shemful_user != "":
            coindelta = amount
            if cointype == "coin":
                coins = self.change_currency("shem", shemful_user, cointype, lambda x: x+coindelta)
                self.save_only()
                await self.client.send_message(channel,\
                    "that gets you {0:.1f} coins! {1} now has {2:.1f} shem coins".format(coindelta, shemful_user, coins))

            elif cointype == "exp":
                currs = self.change_currency("shem", shemful_user, cointype, lambda x: x+coindelta)
                level = self.change_currency("shem", shemful_user, "level", lambda x: x)
                levelcurr = 150+10*level**2 + 10*level
                await self.client.send_message(channel,\
                    "{0} gains {1} exp! to the total of {2}/{3}".format(shemful_user, coindelta, currs, levelcurr))

                if levelcurr < currs:
                    level = self.change_currency("shem", shemful_user, "level", lambda x: x+1)
                    newcurrs = self.change_currency("shem", shemful_user, cointype, lambda x: x-levelcurr)
                    await self.client.send_message(channel,\
                        "You leveled up! {0}'s infinite wisdom has reached level {1}! A change awaits you in hangman.".format(shemful_user, level))

                self.save_only()
            else:
                currs = self.change_currency("shem", shemful_user, cointype, lambda x: x+coindelta)
                self.save_only()
                await self.client.send_message(channel,\
                    "that gets you {0:.1f} {1}!{4}\n{2} now has {3:.1f} {1}".format(coindelta, emoji, shemful_user, currs, flavor))

    def change_currency(self, shem, shemful_user, currency, function):
        if shem not in self.data:
            self.data[shem] = {}
        if shemful_user not in self.data[shem]:
            self.data[shem][shemful_user] = {}
        if currency not in self.data[shem][shemful_user]:
            self.data[shem][shemful_user][currency] = 0
        self.data[shem][shemful_user][currency] = function(self.data[shem][shemful_user][currency])
        if currency == "level" and self.data[shem][shemful_user][currency] == 0:
            self.data[shem][shemful_user][currency] = 1
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
                coindelta = 0
                matcher1 = re.match(r".*Winner.*.*\*\*(\w+\#\d+)\*\*", embed)
                matcher3 = re.match(r".*\'(\w+\#\d+) guessed a letter.*", embed)
                if matcher1:
                    shemful_user = matcher1.group(1)
                    coindelta = 5000
                if matcher3:
                    shemful_user = matcher3.group(1)
                    coindelta = 20
                    
                if shemful_user != "": 
                    
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x+coindelta)
                    self.save_only()
                    await self.client.send_message(message.channel,\
                        "that gets you {0:.1f} coins! {1} now has {2:.1f} shem coins".format(coindelta, shemful_user, coins))
                        
                    loves = self.change_currency("shem", shemful_user, "love", lambda x: x+1)
                    await self.client.send_message(message.channel,\
                        "that also gets you {0:.1f} love! {1} now has {2:.1f} ❤️".format(1, shemful_user, loves))
                    await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=300)
                    
        chen_command = ""
        matcher = re.match(self.prefix + r"(.+)", message.content)
        if matcher:
            chen_command = matcher.group(1)

        if self.restricted_channel is not None and message.channel == self.restricted_channel:
            return
        
        if chen_command.startswith("restrict"):
            if self.restricted_channel is None:
                self.restricted_channel = message.channel
                await self.client.send_message(message.channel, "😶")
            else:
                self.restricted_channel = None
                await self.client.send_message(message.channel, "😄 restriction gone!")

        elif chen_command.startswith("help"):
            commands = [
                "Commands are:",
                ' ',
                '**GENERAL**',
                '**{prefix}help** this command',
                '**{prefix}honk** HONK',
                '**{prefix}meme** inspire people through memes',
                '**{prefix}pomf** do a pomf',
                '**{prefix}roll <number>** roll a number',
                '**{prefix}pat** pat chen',
                '**{prefix}prefix \"<prefix>\"** change prefix',
                '**{prefix}police** monitor a channel for image posting',
                '**{prefix}restrict** disable certain chen commands in a channel',
                ' ',
                '**STALKING**',
                '**{prefix}stalk <user>** to learn about users',
                '**{prefix}keep <user> <data>** to keep data about users',
                '**{prefix}rem <MM-DD> <greeting>** remember a birthday',
                '**{prefix}tz <Tz/Formatted_Timezone>** store your timezone',
                '**{prefix}time** check your time',
                '**{prefix}time User#1234** check a user\'s time',
                ' ',
                '**GAMES**',
                '**{prefix}daily** get daily coins',
                '**{prefix}hangman** play hangman for coins',
                '**{prefix}gacha** get items',
                '**{prefix}bestgirl** who is bestgirl?',
                '**{prefix}lex help** for the lexicant game',
                ' ',
                '**EXCLUSIVES**',
                '**{prefix}critique** critique arts',
                '**{prefix}prompt** drawing prompts',
                ' ',
                '**UNAVAILABLE**',
                '**{prefix}resistance help** for the resistance game',
            ]
            output = '\n'.join(commands).replace('{prefix}', self.prefix)
            await self.client.send_message(message.channel, "Sent the commands help in the pms!")
            await self.client.send_message(message.author, output)
        
        elif chen_command.startswith("rem"):
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

        elif chen_command.startswith("whisper"):
            if message.author.name == "tastelikenyan":
                await self.client.send_message(message.author, "status:\n" + self.status_report)
                self.status_report = ""
            else:
                await self.client.send_message(message.author, "ʷʰᶦˢᵖᵉʳ")
            self.greet_channel = message.channel

        elif chen_command.startswith("honk"):
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
            coindelta = 500

            msg = ""
            if shemful_user not in self.dailies:
                if random.randint(0, 5) == 0:
                    coindelta = 2000
                    msg = "Lucky! "
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x+coindelta)
                self.save_only()
                await self.client.send_message(message.channel,\
                    "You gained {0:.1f} coins!\n{1}{2} now has {3:.1f} shem coins".format(coindelta, msg, shemful_user, coins))
                self.dailies.append(shemful_user)
                await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=100)
            else:
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                await self.client.send_message(message.channel,\
                    "You already claimed! {0} has {1:.1f} shem coins.".format(shemful_user, coins))

        elif chen_command.startswith("gacha"):
            shemful_user = message.author.name + "#" + message.author.discriminator

            totalcoins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
            if totalcoins >= 10000:
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x*0.70)
                await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins due to corporate tax (30%).".format(shemful_user, coins))
                
            if chen_command == "gacha level1":
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                choices = ["kokeshi", "chime", "splash"]

                getted = random.choice(choices)
                if coins < 500:
                    await self.client.send_message(message.channel, "Not enough coins")
                    getted = ""
                else:
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-500)
                    await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=100)

                if getted == "splash":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "💦", amount=1, flavor=" splash(💦) does nothing. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "kokeshi":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🎎", amount=1, flavor=" kokeshi(🎎) does nothing. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
    
                if getted == "chime":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🎐", amount=1, flavor=" chime(🎐) makes you lucky. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))


            elif chen_command == "gacha level2":
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                getted = random.choice(["kokeshi", "candle", "cat", "dog", "rat", "malaysian"])
                if coins < 1000:
                    await self.client.send_message(message.channel, "Not enough coins. needs 1,000")
                    getted = ""
                else:
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-1000)
                    await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=200)
                
                if getted == "kokeshi":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🎎", amount=1, flavor=" kokeshi(🎎) does nothing. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "candle":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🕯", amount=1, flavor=" candle(🕯) lights up things. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "cat":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "😼", amount=1, flavor=" cats(😼) are cute. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "dog":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐶", amount=1, flavor=" dogs(🐶) are adorbs. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "rat":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐀", amount=1, flavor=" rats(🐀) are nice. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "malaysian":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🇲🇾", amount=1, flavor=" good at shitposting. Very friendly. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

            elif chen_command == "gacha level3":
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                getted = random.choice(["kokeshi", "rosary", "harambe", "bear", "freedom"])
                if coins < 1500:
                    await self.client.send_message(message.channel, "Not enough coins. Needs 1,500")
                    getted = ""
                else:
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-1500)
                    await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=300)

                if getted == "kokeshi":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🎎", amount=1, flavor=" kokeshi(🎎) does nothing. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
    
                if getted == "rosary":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "📿", amount=1, flavor=" rosary(📿) increases your holiness. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "harambe":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🦍", amount=1, flavor=" RIP harambe (🦍). ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                    
                if getted == "bear":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐻", amount=1, flavor=" Bears (🐻) are huggable and fierce. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "freedom":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🦅", amount=1, flavor="🦅 FREEDOM 🦅. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))


            elif chen_command == "gacha level4":
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                getted = random.choice(["splash", "knife", "serval", "megumin", "penguin", "toki", "owl", "kaban"])
                if coins < 2000:
                    await self.client.send_message(message.channel, "Not enough coins. Needs 2,000")
                    getted = ""
                else:
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-2000)
                    await self.addCoinsFunc(message.channel, shemful_user, "exp", amount=400)

                if getted == "splash":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "💦", amount=1, flavor=" splash(💦) does nothing. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
    
                if getted == "knife":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🔪", amount=1, flavor=" knife(🔪) is very sharp. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "serval":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐱", amount=1, flavor="Serval(🐱) is Tanoshii! ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                    
                if getted == "megumin":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "💥", amount=1, flavor=" Megumins(💥) destroy property. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "toki":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐦", amount=1, flavor="Crested Ibis(🐦) sings well. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

                if getted == "penguin":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🐧", amount=1, flavor="Emperor Penguins(🐧) give out idol points. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "owl":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🦉", amount=1, flavor="Northern White-faced Owl(🦉) coo-coo. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
                
                if getted == "kaban":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "👒", amount=1, flavor="Kaban-chan(👒) is your friend. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))
        

            elif chen_command == "gacha level5":
                coins = self.change_currency("shem", shemful_user, "coin", lambda x: x)
                choices = ["japan"]

                getted = random.choice(choices)
                if coins < 5000000000:
                    await self.client.send_message(message.channel, "Not enough coins. you need 5,000,000,000")
                    getted = ""
                else:
                    coins = self.change_currency("shem", shemful_user, "coin", lambda x: x-5000000000)

                if getted == "japan":
                    await self.addCoinsFunc(message.channel, shemful_user, getted, "🗾", amount=1, flavor=" Japan(🗾) is a freaking nation. ")
                    await self.client.send_message(message.channel, "{0} now has {1:.1f} shem coins.".format(shemful_user, coins))

            else:
                await self.client.send_message(message.channel,\
                    "type '{0}gacha level1' or '{0}gacha level2' etc. to roll! uses up 500 x level# coins. There are 5 levels.".format(self.prefix))
                await self.client.send_message(message.channel,\
                    "type '{0} inventory' to check your inventory.\ncoin bonuses have been killed.".format(self.prefix))


        elif chen_command.startswith("inventory"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            string_out = ""

            dicts = {
                "coin": "coin",
                "kokeshi":"🎎",
                "chime":"🎐",
                "cat":"😼",
                "dog":"🐶",
                "rat":"🐀",
                "malaysian":"🇲🇾",
                "rosary":"📿",
                "candle":"🕯",
                "knife":"🔪",
                "harambe":"🦍",
                "bear":"🐻",
                "freedom":"🦅",
                "splash":"💦",
                "serval":"🐱",
                "megumin":"💥",
                "japan": "🗾",
                "penguin":"🐧",
                "toki":"🐦",
                "love":"❤️",
                "owl":"🦉",
                "exp":"exp🤔",
                "level":"level",
            }

            for key in dicts.keys():

                currs = self.change_currency("shem", shemful_user, key, lambda x: x)
                if currs != 0:
                    string_out += "{0:.1f} {1}\n".format(currs, dicts[key])

            await self.client.send_message(message.channel, string_out)


        elif chen_command.startswith("bestgirl"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            
            matcher = re.match(r"bestgirl ([a-zA-Z 0-9]+)", chen_command)
            if matcher:
                girl = matcher.group(1)
                coins = self.change_currency("shem", shemful_user, "love", lambda x: x)
                if coins < 1:
                    await self.client.send_message(message.channel, "Not enough love")
                else:
                    coins = self.change_currency("shem", shemful_user, "love", lambda x: x-1)
                    bestkey = "bestgirl"
                    if bestkey not in self.data:
                        self.data[bestkey] = {}
                    if girl not in self.data[bestkey]:
                        self.data[bestkey][girl] = 0
                    self.data[bestkey][girl] += 1
                    self.save_only()
                    await self.client.send_message(message.channel,\
                        "{0} now has {1} bestgirl votes.".format(girl, self.data[bestkey][girl]))
            else:
                bestkey = "bestgirl"
                listing = ""
                if bestkey not in self.data:
                    self.data[bestkey] = {}
                    listing = "No best girl yet.\n"
                else:
                    sorted_girls = sorted(self.data[bestkey].items(), key=operator.itemgetter(1))
                    sorted_girls.reverse()
                    listing = "Best Girl Ranking:\n"
                    for i in range(5):
                        if len(sorted_girls) <= i:
                            break
                        else:
                            listing += "{0}) {1}\n".format(i+1, sorted_girls[i][0])

                await self.client.send_message(message.channel,\
                    "{0}\ntype '{1}bestgirl <xxx>' to also vote. costs 1 love".format(listing, self.prefix))


        elif chen_command.startswith("tz"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            matcher = re.match(r"tz ([a-zA-Z_\/]+)( )?.*", chen_command)
            
            if len(message.mentions) == 1:
                shemful_user = message.mentions[0].name + "#" + message.mentions[0].discriminator
            if matcher:
                timezone = matcher.group(1)
                try:
                    self.change_currency("misc", shemful_user, "tz", lambda x: timezone)
                    now = datetime.datetime.now(pytz.timezone(timezone))
                    await self.client.send_message(message.channel, "nice timezone! got it")
                except pytz.exceptions.UnknownTimeZoneError:
                    await self.client.send_message(message.channel, "notvalid timezone.")
            self.save_only()

        elif chen_command.startswith("time"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            matcher = re.match(r"time (.+\#.+)", chen_command)

            if matcher:
                shemful_user = matcher.group(1)
            if len(message.mentions) == 1:
                shemful_user = message.mentions[0].name + "#" + message.mentions[0].discriminator
            try:
                timezone = self.change_currency("misc", shemful_user, "tz", lambda x: x)
                if timezone == 0:
                    timezone = ""
                now = datetime.datetime.now(pytz.timezone(timezone))
                new_minute = now.minute
                if new_minute < 10:
                    new_minute = "0"+str(new_minute)
                else:
                    new_minute = str(new_minute)
                if 0 <= now.hour and now.hour <= 4:
                    await self.client.send_message(message.channel, "Pls sleep {0}! it's 0{1}:{2}".format(shemful_user, now.hour, new_minute))
                elif 4 <= now.hour and now.hour <= 9:
                    await self.client.send_message(message.channel, "Ohayou {0}-san! it's 0{1}:{2}".format(shemful_user, now.hour, new_minute))
                elif 10 <= now.hour and now.hour <= 11:
                    await self.client.send_message(message.channel, "Hey {0}, Nice morning! it's {1}:{2}".format(shemful_user, now.hour, new_minute))
                elif 12 <= now.hour and now.hour <= 12:
                    await self.client.send_message(message.channel, "{0}. It's high noon. {1}:{2}".format(shemful_user, now.hour, new_minute))
                elif 19 <= now.hour and now.hour <= 24:
                    await self.client.send_message(message.channel, "Konbanwa {0}-san! it's {1}:{2}".format(shemful_user, now.hour, new_minute))
                else:
                    await self.client.send_message(message.channel, "Good day {0}, it's {1}:{2}".format(shemful_user, now.hour, new_minute))

            except pytz.exceptions.UnknownTimeZoneError:
                await self.client.send_message(message.channel, "Pls register your timezone. e.g. {0}tz US/Pacific".format(self.prefix))

        elif chen_command.startswith("police"):
            if self.police_channel is None:
                self.police_channel = message.channel
                await self.client.send_message(message.channel, "serve and protect 🚓")
            else:
                self.police_channel = None
                await self.client.send_message(message.channel, "removing police 🚓")

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
        
        elif chen_command.startswith("hangman"):
            shemful_user = message.author.name + "#" + message.author.discriminator
            level = self.change_currency("shem", shemful_user, "level", lambda x: x)
            await self.hangman.begin(message.channel, level)
        
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
        if self.hangman.state == "game" and message.channel == self.hangman.channel:
            await self.hangman.next(message.content, message.author)
        
        if self.police_channel is not None and message.channel == self.police_channel:
            if len(message.attachments) > 0:
                await self.client.send_message(message.channel, "do not post images here 🚓")
                self.police_channel = None
                await asyncio.sleep(120)
                self.police_channel = message.channel
                # refactory period


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
