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
    usedletters = ""
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
        "Hikigaya Hachiman",
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
        "Souryuu Asuka Langley",
        "Ayanami Rei",
        "Ikari Shinji",
        "Akemi Homura",
        "Kaname Madoka",
        "Sakura Kyouko",
        "Miki Sayaka",
        "Tomoe Mami",
        "Chitoge Kirisaki",
        "Kosaki Onodera",
        "Marika Tachibana",
        "Seishiro Tsugumi",
        "Yui Kanakura",
        "Kousaka Kirino",
        "Aragaki Ayase",
        "Gokou Ruri",
        "Makishima Saori",
        "Kanna Kamui",
        "Kobayashi",
        "Tohru",
        "Elma",
        "Quetzalcoatl",
        "Fafnir",
        "Tamura Manami",
        "Nagato Yuki",
        "Megumin",
        "Aqua",
        "Dustiness Ford Lalatina",
        "Ryuuko Matoi",
        "Mankanshoku Mako",
        "Fujioka Haruhi",
        "Haninozuka Mitsukuni",
        "Hitachiin Kaoru",
        "Hitachiin Hikaru",
        "Morinozuka Takashi",
        "Ootori Kyouya",
        "Suou Tamaki",
        "Akame",
        "Littner Yoko",
        "Shiina Mayuri",
        "Nikiforov Victor",
        "Hazuki Nagisa",
        "Matsuoka Rin",
        "Nanase Haruka",
        "Tachibana Makoto",
        "Ryuugazaki Rei",
        "Brando Dio",
        "Katsuki Yuuri",
        "Plisetsky Yuri",
        "Suzukaze Aoba",
        "Takimoto Hifumi",
        "Takanashi Rikka",
        "Nibutani Shinka",
        "Dekomori Sanae",
        "Illyasviel von Einzbern",
        "Sakura Chiyo",
        "Trabant Chaika",
        "Oumae Kumiko",
        "Kousaka, Reina",
        "Kawashima, Sapphire",
        "Katou Hazuki",
        "Tieria Erde",
        "Lockon Stratos",
        "Lee Ranka",
        "Aioi Yuuko",
        "Naganohara Mio",
        "Shinonome Nano",
        "Izumi Konata",
        "Anarchy Stocking",
        "Demon Kneesocks",
        "Kiyoura Setsuna",
        "Miyazono Kaori",
        "Miyamori Aoi",
        "Yasuhara Ema",
        "Imai Midori",
        "Sakaki Shizuka",
        "Kuroki Tomoko",
        "Yuuki Asuna",
        "Kirigiri Kyouko",
        "Enoshima Junko",
        "Fujisaki Chihiro",
        "Fukawa Touko",
        "Maizono Sayaka",
        "Bernie Sanders",
        "Donald Trump",
        "Adolf Hitler",
        "Hillary Clinton",
        "Barack Obama",
        "Joe Biden"
        "Cat",
        "Ia",
        "Hatsune Miku",
        "Kagamine Rin",
        "Kagamine Len",
        "Megpoid Gumi",
        "Megurine Luka",
        "Kaito",
        "Kizuna Ai",
        "Mitsuha"
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
        self.usedletters = ""

        for i in range(len(self.word)):
            if ord('a') <= ord(self.word[i].lower()) and ord(self.word[i].lower()) <= ord('z'):
                pass
            else:
                l = list(self.cleared)
                l[i] = " "
                self.cleared = "".join(l)
        await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Best Girl Hangman begins!\n{0}\nHP: 100\nWho is this best girl? type a letter to guess!".format(self.cleared)))

    async def next(self, letter, author):
        if len(letter) != 1:
            return
            
        letter = letter.lower()
        if ord('a') <= ord(letter) and ord(letter) <= ord('z'):
            pass
        else:
            return
        shemful_user = author.name + "#" + author.discriminator
        
        hits = 0
        left = 0

        self.usedletters += letter.upper()

        for i in range(len(self.word)):
            if letter[0] == self.word.lower()[i]:
                if self.cleared[i] != letter[0]:
                    hits += 1
                l = list(self.cleared)
                l[i] = self.word[i]
                self.cleared = "".join(l)

            elif self.cleared[i] == "–":
                left += 1
        
        if hits == 0:
            self.health -= 30
            
            if self.health <= 0:
                self.end()
                await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Your best girl died. It's:\n{0}".format(self.word)))
                return

            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="No letters match...\n{0}\nHP: {1}. 30 damage.\nUsed: {2}, type a letter to guess!".format(self.cleared.upper(), self.health, self.usedletters)))

        else:
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="A match!\n{0}\nHP: {1}.\nUsed: {2}, type a letter to guess!".format(self.cleared.upper(), self.health, self.usedletters)))

        if left == 0:
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="Your best girl lives! It's\n{0}".format(self.cleared)))
            if self.state == "none":
                return
            self.end()
            await self.addCoinsFunc(self.channel, shemful_user)


    def end(self):
        self.position = 0
        self.state = "none"
