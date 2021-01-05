import discord
from discord.ext import commands
import random
import time
import copy
import asyncio
import financial

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='^',intents=intents)

testint=0

if testint==0:
    token="Nzg1NzAxNzM4NTAyMDI5MzQz.X87rxA.J8Qlt9Gp6emOGDFk7bQ9INkrRZc"
if testint==1:
    token="Nzg1NDAyODI0MjU4NzQ4NDM3.X83VYQ.ndbOeUlVf5nvPCawQ3HxqbppF-E"

def cardpick():
    global card
    temp=random.choice(card)
    card.remove(temp)

    return temp

defaultcard=[1,2,3,4,5,6,7,8,9,10]
card=[]



@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'TEST'))



matching=[]
processing=[]
process=0
turn=0
user=[]
nickname=[]
playercard=[]

def GetNickname(ids,ctx):
    rpn=[]
    filelines=""

    with open(f"data/user_info{ctx.guild.id}","r") as f :
        filelines=f.readlines()


    for oneid in ids :
        for line in filelines :
            user=line.split(',')
            if user[2]==str(oneid):
                rpn.append(user[1])
    if len(rpn)!=2:
        return -1

    return rpn


turn=0
usercard=[0,0]
channel=None
@bot.command()
async def 대결(ctx) :
    global process
    global matching
    global processing
    global card
    global defaultcard
    global user
    global turn
    global usercard
    global playercard
    global nickname
    global channel

    

    if process==1 :
        await ctx.author.send("이미 진행중인 경기가 있습니다.")
        return

    if ctx.author.id in matching:
        await ctx.author.send("이미 매칭중입니다.")
        return
        
    matching.append(ctx.author.id)
    if len(matching)<2 :
        await ctx.author.send("1대1 대결 매칭중입니다...")
    else :
        process=1
        guild=ctx.guild
        user=[bot.get_user(matching[0]),bot.get_user(matching[1])]
        
        processing.append(matching[0])
        processing.append(matching[1])
        nickname=GetNickname(processing,ctx)
        if nickname==-1:
            await ctx.send("가입을 안한 사람이 있습니다.")
            matching.clear()
        matching.clear()
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user[0]: discord.PermissionOverwrite(read_messages=True,send_messages=True),
            user[1]: discord.PermissionOverwrite(read_messages=True,send_messages=True),         
        }
        turn=random.randint(0,1)

        channel = await guild.create_text_channel("1대1_대결", overwrites=overwrites)
        await channel.send(f"{nickname[turn]}의 차례입니다.")
                    
        if len(card)==0 :
            card=copy.deepcopy(defaultcard)
        playercard.append(cardpick())
        playercard.append(cardpick())

        print(f"p1 : {playercard[1]}")
        print(f"p2 : {playercard[0]}")
        print(len(card))

        await user[0].send(f"상대의 숫자는 {playercard[1]}입니다.")
        await user[1].send(f"상대의 숫자는 {playercard[0]}입니다.")

stack=[0,0]

@bot.command()
async def 베팅(ctx,price) :
    global process
    global processing
    global stack
    global turn
    global nickname
    global channel

    if ctx.author.id in processing:
        if channel!=ctx.channel:
            return

        if ctx.author.id==processing[turn]:
            canbet=financial.givemoney(ctx,nickname[turn],price,3)
            if canbet==-1:
                await ctx.author.send("자신 보유액보다 많이 베팅할수 없습니다.")
                return
            else :
                if int(price)>5000:
                    await ctx.author.send("5000모아를 넘길수 없습니다.")
                    return
                stack[turn]+=int(price)
                if turn==0:
                    turn=1
                else :
                    turn=0
                await channel.send(f"{nickname[turn]}의 차례입니다.({sum(stack)})")
                
        else :
            await ctx.author.send("상대방의 턴입니다.")
    else :
        await ctx.author.send("사용할 수 없는 명령어입니다.")
        return


@bot.command()
async def 포기(ctx) :
    global nickname
    global processing
    global turn
    global channel
    if ctx.author.id in processing:
        if channel!=ctx.channel:
            return


        if ctx.author.id==processing[turn]:
            #내 카드가 상대카드보다 숫자가 더 큰지 확인
            if turn==CardCheck():
                if turn==1:
                    print(nickname[0])
                    financial.givemoney(ctx,nickname[0],sum(stack))
                else:
                    print(nickname[1])
                    financial.givemoney(ctx,nickname[1],sum(stack))
            else:
                financial.givemoney(ctx,nickname[turn],int(stack[turn]/2))
                stack[turn]-=int(stack[turn]/2)
                if turn==1:
                    print(nickname[0])
                    financial.givemoney(ctx,nickname[0],sum(stack))
                else:
                    print(nickname[1])
                    financial.givemoney(ctx,nickname[1],sum(stack))
            await channel.delete()
        else :
            await ctx.author.send("상대방의 턴입니다.")
    else :
        await ctx.author.send("사용할 수 없는 명령어입니다.")
        return


def CardCheck() :
    global playercard
    if playercard[0]>playercard[1]:
        return 0
    else :
        return 1
bot.run(token)