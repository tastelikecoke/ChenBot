import json
import sys
import discord

from honker import Honker

class Chen:
    """ main bot """

    def __init__(self):
        self.client = discord.Client()
        self.secrets = {}
        self.word_data = ""
        self.honkers = {}
        self.load()

        @self.client.event
        async def on_ready():
            """ what happens at start """
            print('Logged in as {0}'.format(self.client.user.name))
            sys.stdout.flush()

        @self.client.event
        async def on_message(message):
            """ what happens on message """
            honker = None
            if not message.server:
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

        self.client.run(self.secrets["token"])

    def load(self):
        """ load datas """
        with open("data/secrets.json", "r") as secrets_file:
            self.secrets = json.loads(secrets_file.read())
        with open("data/words.txt", "r") as word_data_file:
            self.word_data = word_data_file.read()

if __name__ == "__main__":
    Chen()