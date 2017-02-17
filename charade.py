import asyncio
import random
import re

class Charade:
    word = ""
    words = ""
    state = "none"
    channel = None
    sendMessageFunc = lambda x, y: None

    def __init__(self, sendMessageFunc, words):
        self.sendMessageFunc = sendMessageFunc
        self.words = words

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    async def begin(self, user, channel):
        self.channel = channel
        self.state = "game"
        self.word = random.choice(self.words)
        await self.sendMessage(user, "word is {0}".format(self.word))
        await self.sendMessage(self.channel, "charades begin!\n type your guesses as single words (but not you game starter you have to type emojis only)")

    async def guess(self, word, user):
        if word == self.word:
            await self.sendMessage(self.channel, "honk {0} is the correct word! thanks {1}".format(word, user))
            self.end()

    async def end(self):
        self.word = ""
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
#             await r.begin(x.split(" ")[1], )
#         if x.startswith("guess"):
#             await r.append(x.split(" ")[1])
#         if x.startswith("seerit"):
#             await r.seerit()
# def Test():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())

# Test()
