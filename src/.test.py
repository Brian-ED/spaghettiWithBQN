import random
async def f(msg, command, prefix):
    smashorpass = False
    with open("sop.COMMUNICATIONSARRAY") as f:
        sopfile = f.readlines()
    if command == prefix+"smashorpass" and len(msg.content.split()) <2:
        for line in range(len(open("sop.COMMUNICATIONSARRAY").readlines())):
            sopfile[line - 1].split(",")
        sop_creature = random.randint(0,7)
        await msg.channel.send(f"Smash -- or -- Pass\n{sopfile[sop_creature][2]}")
        await msg.channel.send(sopfile[sop_creature][3])
        await msg.channel.send(f"{prefix}smash - {prefix}pass")
        smashorpass = True
    if msg.content.removeprefix(prefix) == "smash" and smashorpass == True:
        for line in sopfile:
            line.split(",")
        await msg.channel.send(sopfile[sop_creature][2])
        await msg.channel.send(sopfile[sop_creature][3])
        await msg.channel.send(f"""You Said: **smash**
You agree with {round((int(sopfile[sop_creature][0]) / int((sopfile[sop_creature])[1])) * 100)}% of people ({int(sopfile[sop_creature][0])} people)
{prefix}smash - {round((int(sopfile[sop_creature][0]) / int((sopfile[sop_creature])[1])) * 100)}% ({int(sopfile[sop_creature][0])})  {prefix}pass - {round((int(sopfile[sop_creature][1]) / int((sopfile[sop_creature])[0])) * 100)}% ({int(sopfile[sop_creature][0])})""")
        with open("sop.COMMUNICATIONSARRAY.temp",'w') as f:
            f.write(''.join(sopfile))
        soptemp = open("sop.COMMUNICATIONSARRAY.temp").readlines()
        for line in range(len(open("sop.COMMUNICATIONSARRAY.temp").readlines())):
            soptemp[line - 1].split(",")
        soptemp[sop_creature][0] = int(soptemp[sop_creature][0])+1
        open("sop.COMMUNICATIONSARRAY.temp").write(str(soptemp))
        open("sop.COMMUNICATIONSARRAY").write(str(open("sop.COMMUNICATIONSARRAY.temp")))
        smashorpass = False
    if msg.content.removeprefix(prefix) == "pass" and smashorpass == true:
        sopfile = open("sop.COMMUNICATIONSARRAY").readlines()
        for line in range(len(open("sop.COMMUNICATIONSARRAY").readlines())):
            sopfile[line - 1].split(",")
        await msg.channel.send(sopfile[sop_creature][2])
        await msg.channel.send(sopfile[sop_creature][3])
        await msg.channel.send(f"""You Said: **pass**
    You agree with {round((int(sopfile[sop_creature][1]) / int((sopfile[sop_creature])[0])) * 100)}% of people ({int(sopfile[sop_creature][0])} people)
    {prefix}smash - {round((int(sopfile[sop_creature][0]) / int((sopfile[sop_creature])[1])) * 100)}% ({int(sopfile[sop_creature][0])})  {prefix}pass - {round((int(sopfile[sop_creature][1]) / int((sopfile[sop_creature])[0])) * 100)}% ({int(sopfile[sop_creature][0])})""")
        open("sop.COMMUNICATIONSARRAY.temp").write(str(open("sop.COMMUNICATIONSARRAY").read))
        soptemp = open("sop.COMMUNICATIONSARRAY.temp").readlines()
        for line in range(len(open("sop.COMMUNICATIONSARRAY.temp").readlines())):
            soptemp[line - 1].split(",")
        soptemp[sop_creature][1] = int(soptemp[sop_creature][0])+1
        open("sop.COMMUNICATIONSARRAY.temp").write(str(soptemp))
        open("sop.COMMUNICATIONSARRAY").write(str(open("sop.COMMUNICATIONSARRAY.temp")))
        smashorpass = False