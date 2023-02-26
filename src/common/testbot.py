import discord as dis
from yaml import safe_load
import BQN
comm = BQN.CreateComm("discBot", pathToBQNScript="testbot.bqn")

comm.SendMsg("Hellooo")
print(comm.GetMsg(1))

client = dis.Client()
@client.event
async def on_ready():
    print("READY")

@client.event
async def on_message(msg:dis.Message):
    if msg.author.bot or msg.guild.id!=831963301289132052:
        return
    comm.SendMsg(msg.content)
    await msg.channel.send(comm.GetMsg(1))

safe = r"C:/Users/brian/OneDrive - Klaksvíkar Tekniski Skúli/Persinal/discBots/Safe/Fire-Owl-bot.yaml"
with open(safe, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])