import asyncio
import random
import re

class Lexicant:
    """ lexicant commands """

    word = ""
    words = ""
    state = "none"
    channel = None
    sendMessageFunc = lambda x, y: None

    def __init__(self, sendMessageFunc):
        self.sendMessageFunc = sendMessageFunc

        with open("data/words.txt", "r") as words_file:
            self.words = words_file.read()

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    async def begin(self, word, channel):
        self.channel = channel
        if len(word) != 1:
            await self.sendMessage(self.channel, "not valid length.")
            return
        self.state = "game"
        self.word = word
        await self.sendMessage(self.channel, "word: {0}".format(self.word))
        await self.sendMessage(self.channel, "start saying words")

    async def append(self, word):
        if self.state != "game":
            return
        if len(word) == 0:
            await self.sendMessage(self.channel, "no game.")
            return
        if len(word) != len(self.word)+1:
            return
        if self.word not in word:
            return
        if word not in self.words:
            await self.sendMessage(self.channel, "not part of a word.")
            return
        if len(word) > 3 and "\n"+word+"\n" in self.words:
            await self.sendMessage(self.channel, "A word! you lose!")
            await self.end()
            return
        self.word = word
        await self.sendMessage(self.channel, "word: {0}".format(self.word))
    async def seerit(self):
        closest = re.search("\n.*"+self.word+".*\n", self.words)
        await self.sendMessage(self.channel, "closest:{0}".format(closest.group()))
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
