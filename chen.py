import json
import sys
import asyncio
import discord

from honker import Honker

class Peem:
    async def ask(self, message):
        if not message.author.name.startswith("tastelikenyan"):
            return

        if message.content.startswith("transfer"):
            all_data = {}
            with open("data/data.json", "r") as data_file:
                all_data = json.loads(data_file.read())

                for server_key in all_data.keys():
                    try:
                        for user_key in all_data[server_key]["shem"].keys():
                            user_coins = all_data[server_key]["shem"][user_key]
                            if user_coins is not dict:
                                all_data[server_key]["shem"][user_key] = {"coin": int(user_coins*100)}
                    except KeyError as e:
                        print(e)

            with open("data/data.json", "w") as data_file:
                data_file.write(json.dumps(all_data))


class Chen:
    """ main bot """

    def __init__(self):
        self.client = discord.Client()
        self.secrets = {}
        self.word_data = ""
        self.honkers = {}
        self.peem = Peem()
        self.load()

        @self.client.event
        async def on_ready():
            """ what happens at start """
            print('Logged in as {0}'.format(self.client.user.name))
            sys.stdout.flush()
            await self.clock()

        @self.client.event
        async def on_message(message):
            """ what happens on message """
            honker = None
            if not message.server:
                await self.peem.ask(message)
                return
            elif message.server.id not in self.honkers:
                honker = Honker(message.server)
                honker.load()
                self.honkers[message.server.id] = honker
            else:
                honker = self.honkers[message.server.id]

            sys.stdout.flush()
            honker.bind_client(self.client)
            await honker.ask(message)
            await self.clock()

        self.client.run(self.secrets["token"])

    async def clock(self):
        for honker in self.honkers:
            await self.honkers[honker].clock()

    def load(self):
        """ load datas """
        with open("data/secrets.json", "r") as secrets_file:
            self.secrets = json.loads(secrets_file.read())
        with open("data/words.txt", "r") as word_data_file:
            self.word_data = word_data_file.read()

if __name__ == "__main__":
    Chen()