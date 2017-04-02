import asyncio
import random
import re
import discord

class Hangman:
    """ hangman commands """

    state = "none"
    position = 0
    channel = None
    sendMessageFunc = lambda x, y: None
    addCoinsFunc = lambda x, y: None
    shemful_user = ""
    cleared = ""
    word = ""
    health = 0

    words = [
        "Kirigaya Kazuto",
        "Makise Kurisu",
        "Gasai Yuno",
        "Aisaka Taiga",
        "Yukinoshita Yukino",
        "Yuigahama Yui",
        "Senjougahara Hitagi",
        "Araragi Koyomi",
        "Hachikuji Mayoi",
        "Hanekawa Tsubasa",
        "Kanbaru Suruga",
        "Sengoku Nadeko",
        "Araragi Karen",
        "Oshino Shinobu",
        "Kaiki Deishuu",
        "Ononoki Yotsugi",
        "Totsuka Saika",
        "Ebina Hina",
        "Isshiki Iroha",
        "Hikigaya Hachiman"
        "Saber",
        "Tousaka Rin",
        "Archer",
        "Gilgamesh",
        "Kotomine Kirei",
        "Matou Sakura",
        "Ayase Eli",
        "Hoshizora Rin",
        "Koizumi Hanayo",
        "Kousaka Honoka",
        "Minami Kotori",
        "Nishikino Maki",
        "Sonoda Umi",
        "Toujou Nozomi",
        "Yazawa Nico",
        "Suzumiya Haruhi",
        "Akiyama Mio",
        "Hirasawa Yui",
        "Kotobuki Tsumugi",
        "Nakano Azusa",
        "Tainaka Ritsu",
        "Rem",
        "Ram",
        "Emilia",
        "Argail Felix",
        "Natsuki Subaru",
        "Beatrice",
        "Felt",
        "Joseph Joestar",
    ]

    def __init__(self, sendMessageFunc):
        self.sendMessageFunc = sendMessageFunc

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    async def begin(self, channel):
        if self.state == "game":
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="already running..."))
            return
        self.channel = channel
        self.state = "game"
        random_word = random.choice(self.words)
        self.cleared = "–" * len(random_word)
        self.word = random_word
        self.health = 100

        for i in range(len(self.word)):
            if self.word[i] == " ":
                l = list(self.cleared)
                l[i] = " "
                self.cleared = "".join(l)
        await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Best Girl Hangman begins!\n{0}\nHP: 100\nWho is this best girl?".format(self.cleared)))

    async def next(self, letter, author):
        if len(letter) != 1:
            return
        letter = letter.lower()
        shemful_user = author.name + "#" + author.discriminator
        
        hits = 0
        left = 0

        for i in range(len(self.word)):
            if letter[0] == self.word.lower()[i]:
                l = list(self.cleared)
                l[i] = self.word[i]
                self.cleared = "".join(l)
                hits += 1
            elif self.cleared[i] == "–":
                left += 1
        
        if hits == 0:
            self.health -= 30
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="No letters match...\n{0}\nHP: {1}. 30 damage.".format(self.cleared.upper(), self.health)))
        else:
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="A match!\n{0}\nHP: {1}.".format(self.cleared.upper(), self.health)))

        if self.health <= 0:
            await self.end()
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Your best girl died. It's:\n{0}".format(self.word)))

        if left == 0:
            await self.end()
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Your best girl lives! It's\n{0}".format(self.cleared)))
            await self.addCoinsFunc(self.channel, shemful_user)


    async def end(self):
        self.position = 0
        self.state = "none"
