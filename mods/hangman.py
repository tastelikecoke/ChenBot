import asyncio
import random
import re
import discord

def dummy(*args, **kargs):
    pass

class Hangman:
    """ hangman commands """

    state = "none"
    position = 0
    channel = None
    sendMessageFunc = dummy
    addCoinsFunc = dummy
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
        "Tamura Manami",
        "Nagato Yuki",
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
        "Shiina Mayuri",
        "Hazuki Nagisa",
        "Matsuoka Rin",
        "Nanase Haruka",
        "Tachibana Makoto",
        "Ryuugazaki Rei",
        "Suzukaze Aoba",
        "Takimoto Hifumi",
        "Takanashi Rikka",
        "Nibutani Shinka",
        "Dekomori Sanae",
        "Izumi Konata",
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
    ]

    words2 = [
        "Brando Dio",
        "Noriaki Kakyoin",
        "Mohammed Avdol",
        "Jotaro Kujo",
        "Jean Pierre Polnareff",
        "Iggy",
        "Hol Horse",
        "J. Geil",
        "ZZ",
        "Steely Dan",
        "Mannish Boy",
        "Daniel J. D'Arby",
        "Terence T. D'Arby",
        "Vanilla Ice",
        "Kenny G",
        "Suzi Q Joestar",
        "Oingo"
        "Katsuki Yuuri",
        "Plisetsky Yuri",
        "Saber",
        "Tohsaka Rin",
        "Archer",
        "Gilgamesh",
        "Kotomine Kirei",
        "Matou Sakura",
        "Aioi Yuuko",
        "Naganohara Mio",
        "Shinonome Nano",
        "Illyasviel von Einzbern",
        "Sakura Chiyo",
        "Trabant Chaika",
        "Oumae Kumiko",
        "Kousaka, Reina",
        "Kawashima, Sapphire",
        "Katou Hazuki",
        "Rem",
        "Ram",
        "Emilia",
        "Argail Felix",
        "Natsuki Subaru",
        "Beatrice",
        "Felt",
        "Souryuu Asuka Langley",
        "Ayanami Rei",
        "Ikari Shinji",
        "Anarchy Stocking",
        "Demon Kneesocks",
        "Bernie Sanders",
        "Donald Trump",
        "Adolf Hitler",
        "Hillary Clinton",
        "Tieria Erde",
        "Lockon Stratos",
        "Nikiforov Victor",
        "Kanna Kamui",
        "Kobayashi",
        "Tohru",
        "Megumin",
        "Aqua",
        "Joseph Joestar",
        "Dustiness Ford Lalatina",
        "Elma",
        "Quetzalcoatl",
        "Fafnir",
        "Littner Yoko",
        "Lee Ranka",
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
        "Mitsuha",
        "Yue",
        "Clow Reed",
        "Cerberus",
        "Sakura Kinomoto",
        "Tomoyo Daidouji",
        "Lee Shaoran",
    ]

    words3 = [
        "Mahiro Yasaka",
        "Nyaruko",
        "Yoriko Yasaka",
        "Tamao Kurei",
        "Cthulhu",
        "Nyarlathotep",
        "Shub-Niggurath",
        "Ghatanothoa",
        "Zoth-Ommog",
        "Derleth",
        "Ubbo-Sathla",
        "Cyaegha",
        "Hastur",
        "Ithaqua",
        "Nyogtha",
        "Cthugha",
        "Dagon",
        "Aphoom-Zhah",
        "R'lyeh",
        "Shoggoth",
        "Mi-go",
        "Amon-Gorloth",
        "Atlach-Nacha",
        "Baoht Z'uqqa-Mogg",
        "B’gnu-Thun",
        "Bokrug",
        "Bugg-Shash",
        "Chaugnar Faugn",
        "Cynothoglys",
        "Dythalla",
        "Etepsed Egnis",
        "Ei'lor",
        "Ghadamon",
        "Gobogeg",
        "Gol-goroth",
        "Groth-Golka",
        "Gurathnaka",
        "Gzxtyos",
        "H’chtelegoth",
        "Hziulquoigmnzhah",
        "Hnarqu",
        "M'Nagalah",
        "Mnomquah",
        "Nctolhu",
        "Nctosa",
        "Nssu-Ghahnb",
        "Psuchawrl",
    ]


    def __init__(self, sendMessageFunc):
        self.sendMessageFunc = sendMessageFunc

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    async def begin(self, channel, level):
        if self.state == "game":
            await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="already running..."))
            return
        self.channel = channel
        
        self.state = "game"
        flavor = ""
        if level >= 30:
            flavor = "Bllyeh-St Girl Cthanghman Normal And Hard Shoggins!"
            random_word = random.choice(self.words3.extend(self.words2.extend(self.words4)))
            self.cleared = "–" * len(random_word)
            self.word = random_word
            self.usedletters = ""
            self.health = 100+level*5

        if level >= 20:
            flavor = "Bllyeh-St Gorgollth Cthanghman Cthulhu Shoggoth!"
            random_word = random.choice(self.words3)
            self.cleared = "–" * len(random_word)
            self.word = random_word
            self.usedletters = ""
            self.health = 100+level*4

        elif level >= 10:
            flavor = "Best Girl Hangman HARDMODE begins!"
            random_word = random.choice(self.words2)
            self.cleared = "–" * len(random_word)
            self.word = random_word
            self.usedletters = ""
            self.health = 100+level*3

        else:
            flavor = "Best Girl Hangman begins!"
            random_word = random.choice(self.words)
            self.cleared = "–" * len(random_word)
            self.word = random_word
            self.usedletters = ""
            self.health = 100+level*2

        

        for i in range(len(self.word)):
            if ord('a') <= ord(self.word[i].lower()) and ord(self.word[i].lower()) <= ord('z'):
                pass
            else:
                l = list(self.cleared)
                l[i] = " "
                self.cleared = "".join(l)
        await self.sendMessage(self.channel, discord.Embed(title="Hangman", description="{0}\n{1}\nHP: {2}\nWho is this best girl? type a letter to guess!".format(flavor, self.cleared, self.health)))

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
            await self.addCoinsFunc(self.channel, shemful_user, "exp", amount=100)

    def end(self):
        self.position = 0
        self.state = "none"
