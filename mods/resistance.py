import asyncio
import random

class Resistance:
    players = []
    roles = {}
    assignees = []
    state = "" # vote -> missioning -> vote
    votes = []
    novotes = []
    current = None
    currentIdx = 0
    channel = None
    missionRatio = [0.5, 0.5, 0.5, 0.7, 0.7]
    missionIdx = 0
    failPoints = 0
    successPoints = 0
    sendMessageFunc = lambda x, y: None

    def __init__(self, sendMessageFunc):
        self.sendMessageFunc = sendMessageFunc

    async def sendMessage(self, channel, message):
        await self.sendMessageFunc(channel, message)

    def sayPlayers(self, players):
        output = ""
        for player in players:
            if type(player) == str:
                output += player + "\n"
            else:
                output += player.name + "\n"
        return output

    def missioneerReq(self):
        req = int(self.missionRatio[self.missionIdx]*float(len(self.players)))
        if req == 0:
            return 1
        return req

    async def begin(self, players, channel):
        self.players = players
        self.channel = channel
        self.votes = []
        self.novotes = []
        self.missionIdx = 0
        await self.sendMessage(self.channel, \
            "Players:\n{}".format(self.sayPlayers(self.players)))
        random.shuffle(self.players)

        ratio = 0.3
        player_ratio = 0
        for player in self.players:
            self.roles[player] = "spy" if ratio > player_ratio else "resistance"
            await self.sendMessage(player, "you are {}".format(self.roles[player]))
            player_ratio += 1.0/float(len(players))

        self.currentIdx = random.randint(0, len(self.players)-1)
        await self.beginAssign()

    async def beginAssign(self):
        self.state = "assign"
        self.votes = []
        self.novotes = []
        self.current = self.players[self.currentIdx]
        self.currentIdx = (self.currentIdx + 1) % len(self.players)
        await self.sendMessage(self.channel, "Mission {}\n{} is assigning.\nuse chen assign".format(self.missionIdx+1, self.current))
        await self.sendMessage(self.channel, "you need to assign {0}".format(self.missioneerReq()))

    async def beginVote(self, assigner, assignees):
        if self.state != "assign":
            return
        if self.current != assigner:
            return
        self.assignees = assignees
        for assignee in assignees:
            if assignee not in self.players:
                await self.sendMessage(self.channel, "pls, players only")
                return
        if len(assignees) != self.missioneerReq():
            await self.sendMessage(self.channel, "pls do it again honk")
            return

        await self.sendMessage(self.channel, "roger!")
        await self.sendMessage(self.channel, "Mission Members:\n" + self.sayPlayers(self.assignees))
        self.votes = []
        self.novotes = []
        self.state = "vote"
        await self.sendMessage(self.channel, "Vote now! to vote: either say chen yes or chen no")

    async def yesVote(self, voter):
        if self.state != "vote":
            return
        if voter not in self.players:
            return
        if voter in self.votes:
            await self.sendMessage(self.channel, "no")
            return
        await self.sendMessage(self.channel, "roger!")
        self.votes.append(voter)
        if len(self.votes) > len(self.players)/2:
            await self.sendMessage(self.channel, "mission greenlight!")
            await self.beginMission()

    async def noVote(self, voter):
        if self.state != "vote":
            return
        if voter not in self.players:
            return
        if voter in self.novotes:
            await self.sendMessage(self.channel, "no")
            return
        await self.sendMessage(self.channel, "roger!")
        self.novotes.append(voter)
        if len(self.novotes) > len(self.players)/2 or len(self.novotes)*2 == len(self.players):
            await self.sendMessage(self.channel, "mission vetoed!")
            await self.beginAssign()

    async def beginMission(self):
        self.state = "mission"
        self.votes = []
        self.novotes = []
        for assignee in self.assignees:
            if self.roles[assignee] == "spy":
                await self.sendMessage(assignee, "vote success? say either chen success or chen fail here")
            else:
                await self.passMission(assignee)

    async def passMission(self, voter):
        if self.state != "mission":
            return
        if voter not in self.assignees:
            return
        if voter in self.votes:
            return
        self.votes.append(voter)
        await self.sendMessage(voter, "you vote success.")
        if len(self.novotes) + len(self.votes) >= len(self.assignees):
            await self.endMission()

    async def failMission(self, voter):
        if self.state != "mission":
            return
        if voter not in self.assignees:
            return
        if voter in self.novotes:
            return
        self.novotes.append(voter)
        await self.sendMessage(voter, "you vote fail.")
        if len(self.novotes) + len(self.votes) >= len(self.assignees):
            await self.endMission()

    async def endMission(self):
        if self.state != "mission":
            return
        if len(self.novotes) > 0:
            await self.sendMessage(self.channel, "Mission Fail.")
            self.failPoints += 1
        else:
            await self.sendMessage(self.channel, "Mission Success!")
            self.successPoints += 1
        await self.sendMessage(self.channel, "fails: {0}, success: {1}".format(self.failPoints, self.successPoints))
        self.missionIdx += 1
        if self.missionIdx >= len(self.missionRatio) or self.failPoints == 3 or self.successPoints == 3:
            await self.sendMessage(self.channel, "Game End.")
            self.missionIdx = 0
        else:
            await self.beginAssign()

# async def main():
#     async def f(x, y):
#         print(y)
#         return
#     r = Resistance(f)
#     while True:
#         x = input()
#         if x.startswith("begin"):
#             await r.begin(x.split(" ")[1:])
#         if x.startswith("assign"):
#             await r.beginVote(x.split(" ")[1], x.split(" ")[2:])
#         if x.startswith("yes"):
#             await r.yesVote(x.split(" ")[1])
#         if x.startswith("no"):
#             await r.noVote(x.split(" ")[1])
#         if x.startswith("pass"):
#             await r.passMission(x.split(" ")[1])
#         if x.startswith("fail"):
#             await r.failMission(x.split(" ")[1])
# def Test():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#
# Test()
