import asyncio
import random
import re

class Eroge:
    """ eroge commands """

    state = "none"
    position = 0
    channel = None
    sendMessageFunc = lambda x, y: None

    prompts = [
        ["Someone is breathing heavily behind you. What do?", "check out"],
        ["Chen appears in front of you. What do?", "honk"],
        ["Chen asks for a pat. What do?", "pat"],
        ["Chen squees in delight as you pat her. What do?", "hug"],
        ["Chen hugs you back. What do?", "invite her"],
        ["Chen goes inside your room. What do?", "hide porn"],
        ["Chen looks under your bed, What do?", "warn her"],
        ["Chen looks at your computer, What do?", "say no"],
        ["Chen looks at your daki collection, What do?", "tour her"],
        ["Chen looks intently at your touhou dakis, What do?", "hold her"],
        ["You are holding chen. What do?", "hold her"],
        ["But you are holding chen..... What do?", "confess"],
        ["You confessed that you like bald old men. What do?", "run away"],
        ["Chen follows you back. What do?", "run fast"],
        ["You are tired. What do?", "get coin"],
        ["You have coin. What do?", "go to vending machine"],
        ["You are at the vending machine. What do?", "PUT IT IN"],
        ["It's stuck. What do?", "JAM IT IN"],
        ["Something falls to the slot below. What do?", "bring soda back"],
        ["You found a dead rat. What do?", "grab it"],
        ["You put the dead rat in your pockets. What do?", "knees heavy"],
        ["You felt the weight of your knees. What do?", "palms sweaty"],
        ["Your hands are covered with sweat. What do?", "wipe it"],
        ["You wipe it in your sweatshirt. You smell like spaghetti. What do?", "moms spaghetti"],
        ["You realize you are in the middle of nowhere. What do?", "lose yourself"],
        ["You miss chen. What do?", "find her"],
    ]
    badresponse = [
        "put it in",
        "put it in",
        "put it in",
        "jam it in",
        "jam it in",
        "jam it in",
        "jam it in",
        "go to soap bath",
        "go to akihabara",
        "can't be helped",
        "bring illya back",
        "genuflect",
        "thank chen",
        "cirno is better",
        "say hi",
        "say yes",
        "put it",
        "kiss her",
        "HONK",
        "let her",
        "get porn",
        "show porn",
        "show dakis",
        "grab her",
        "whisper",
        "ask out",
        "jump on",
        "show her",
        "grab tight"
    ]
    goodchoices = ""
    badchoices = []

    def __init__(self, sendMessageFunc):
        self.sendMessageFunc = sendMessageFunc

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    async def begin(self, channel):
        self.channel = channel
        self.state = "game"
        self.position = 0
        await self.sendMessage(self.channel, "http://i.imgur.com/minQBSp.jpg\n")
        await self.next("", True)

    async def next(self, word, notrigger=False):
        if word in self.badchoices and not notrigger:
            await self.end()
        elif word == self.goodchoices or notrigger:
            self.position += 1
            self.goodchoices = self.prompts[self.position % len(self.prompts)][1]
            self.badchoices = [random.choice(self.badresponse), random.choice(self.badresponse), random.choice(self.badresponse)]
            
            choices = [self.goodchoices,]
            choices.extend(self.badchoices)
            random.shuffle(choices)
            choice = "(a) {0}      (b) {1}\n(c) {2}      (d) {3}".format(*choices)
            
            await self.sendMessage(self.channel, "{0}\n{1}".format(\
                self.prompts[self.position % len(self.prompts)][0],
                choice))

    async def end(self):
        await self.sendMessage(self.channel, "http://i.imgur.com/vJbHB0c.jpg\n BAD END\nSCORE: {0}".format(self.position*238))
        self.position = 0
        self.state = "none"

# async def main():
#     async def f(x, y):
#         print(y)
#         return
#     r = None
#     with open("words.txt", "r") as wordFile:
#         words = wordFile.read()
#         r = Lexicant(f, words, None)
#     while True:
#         x = input()
#         if x.startswith("begin"):
#             await r.begin(x.split(" ")[1])
#         if x.startswith("append"):
#             await r.append(x.split(" ")[1])
#         if x.startswith("seerit"):
#             await r.seerit()
# def Test():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#
# Test()
