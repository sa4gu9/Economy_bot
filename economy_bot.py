# -*- coding: utf-8 -*- 

import discord
from discord.ext import commands
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import string
import math
import os.path
import asyncio
import sched
import datetime

bot = commands.Bot(command_prefix='$')

token=""
version="V1.0.9"
cancommand=True
canLotto=True
getnotice=False

testmode=False
Lottocool=0
Lottomax=3

forceMsg=[]

if testmode :
    giveMcool=1
    Lottocool=1
    token="NzY4MzcyMDU3NDE0NTY1OTA4.X4_gPg.fg2sLq5F1ZJr9EwIgA_hiVHtfjQ"
    version+=" TEST"
    maxlucky=500
    Lottomax=10
else :
    giveMcool=60
    Lottocool=16
    Lottomax=3
    token = "NzY4MjgzMjcyOTQ5Mzk5NjEy.X4-Njg.NfyDMPVlLmgLAf8LkX9p0s04QDY"
    maxlucky=10000000
    
lottoRange=10


@bot.event
async def on_message(tempmessage) :
    global getnotice
    if tempmessage.author.id!=768283272949399612 and tempmessage.channel.id==771203131836989443 and tempmessage.author.id!=768372057414565908 :
        if len(tempmessage.content)>50 :    
            await tempmessage.delete()

    if str(tempmessage.content).startswith('$') :
        if cancommand :
            if tempmessage.channel.id!=771203131836989443 and tempmessage.channel.id!=709647685417697372 :
                await tempmessage.channel.send("봇 전용 채널에서만 사용 가능합니다.")
                return
            else :
                await bot.process_commands(tempmessage)
        else :
            if tempmessage.author.id==382938103435886592 :
                await bot.process_commands(tempmessage)
            else :
                if str(tempmessage.content).startswith('$') :
                    if not getnotice  :
                        channel=bot.get_channel(768343875001516074)
                        await channel.send("현재 일시정지 상태입니다.")
                        getnotice=True                    
                    else :
                        getnotice=False

    

@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'{version} $도움말'))
    bot.loop.create_task(job())

async def job() :
    channel=bot.get_channel(709647685417697372)
    while True:
        currentTime=str(datetime.datetime.now().time())[0:8]
        print(currentTime[0:5])
        print(currentTime[3:5])#분
        print(currentTime[6:8])#초
        if currentTime[0:5]=="01:00" and ( int(currentTime[6:8]) >=0 and int(currentTime[6:8]) <10):
            file=open("forcestore","r")
            file_text=file.read()
            file.seek(0)
            fileLines=file.readlines()
            file.close()


            info1=fileLines[0]
            information=info1.split(',')

            if int(information[1])<100:
                file_text=file_text.replace(f"1,{information[1]}","1,100")
                file=open("forcestore","w")
                file.write(file_text)
                file.close()
                await channel.send("의문의 물건 +1의 남은 개수가 100개가 되었습니다.")
        await asyncio.sleep(10)


@bot.event
async def on_reaction_add(reaction,user) :
    global forceMsg
    if user.bot :
        return

    if reaction.message.id in forceMsg :
        if user.display_name==reaction.message.content :
            if str(reaction.emoji)=="🔨":
                await doforce(reaction.message,user,1)
                forceMsg.remove(reaction.message.id)
                await reaction.message.delete()
            if str(reaction.emoji)=="😀":
                await sellforce(reaction.message,user)
                forceMsg.remove(reaction.message.id)
                await reaction.message.delete()
            if str(reaction.emoji)=="🔥":
                await doforce(reaction.message,user,3)
                forceMsg.remove(reaction.message.id)
                await reaction.message.delete()
            


def get_fail(level):
    temp=0
    for i in range(level) :
        if i==0:
            temp=0
        else :
            temp+=0.1*i

    return temp

def get_need(level):
    temp=[0,0,0,0,0,0]
    temp2=0
    for i in range(level):
        if i<6 :
            temp[i]=1
            temp2=1
        else :
            temp2=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp[4]
            temp[4]=temp[5]
            temp[5]=temp2
    return temp2

async def doforce(message,reuser,count):
    level = 1
    cri_success=0.0
    success=0.0
    not_change=0.0
    fail=0.0
    destroy=0.0
    result=0.0
    change=0

    moa=0
    level=0

    #region 반복 구간 시작

    for i in range(count):
        file=open(f"user_info{message.guild.id}","r")
        file_text=file.read()
        file.seek(0)
        lines=file.readlines()
        file.close()

        ctx=message.channel

        for user in lines :
            user_info=user.split(',')
            if user_info[2]==str(reuser.id):
                level=int(user_info[4])
                moa=int(user_info[3])
                nickname=user_info[1]
        
        need=get_need(level)
        

        if need>moa :
            await ctx.send(f"{need-moa}모아가 부족합니다.")
            return
        if level == 30 :
            await ctx.send("이미 의문의 물건 +30을 가지고 있습니다.")
            return
        elif level == 0 :
            await ctx.send("의문의 물건을 가지고 있지 않습니다.")
            return

        if level !=29 :
            cri_success=0.05*(30-level)
        else :
            cri_success=0.0

        if level<15 :
            destroy=0.0
        else :
            destroy=1.41*(level-29)+20

        success=100-3.2*level
        fail=get_fail(level)

        not_change=100 - cri_success - success - fail - destroy

        result=random.random()*100

        print(result)

        if result<cri_success :
            print(f"{result}  {cri_success}")
            change=2        
        elif result<cri_success + success :
            print(f"{result}  {cri_success+success}")
            change=1
        elif result<cri_success+success + not_change :
            print(f"{result}  {cri_success+success+ not_change}")
            change=0
        elif result < cri_success + success + not_change + fail :
            print(f"{result}  {cri_success+success+ not_change+ fail}")
            change=-1
        else :
            change=-10
        
        print(change)

        if change!=-10 :
            file_text=file_text.replace(f"{reuser.id},{'%010d'%moa},{level}",f"{reuser.id},{'%010d'%(moa-need)},{level+change}")
            if change>0 :
                await ctx.send(f"{nickname}, 강화 레벨 {level}에서 {change} 상승! 현재 레벨 : {level+change}")
            elif change<0 :
                await ctx.send(f"{nickname}, 강화 레벨 {level}에서 {-change} 감소! 현재 레벨 : {level+change}")
            else :
                await ctx.send(f"{nickname}, 강화 레벨 {level}에서 변동 없음! 현재 레벨 : {level}")      
        else :
            file_text=file_text.replace(f"{reuser.id},{'%010d'%moa},{level}",f"{reuser.id},{'%010d'%(moa-need)},0")
            await ctx.send(f"{nickname}, 의문의 물건 +{level} 파괴...")
        
        file=open(f"user_info{ctx.guild.id}","w")
        file.write(file_text)
        file.close()
        asyncio.sleep(0.1)
    #endregion

async def sellforce(message,reuser) :
    ctx=message.channel
    level=0
    before=0
    after=0
    change=0

    file=open(f"user_info{message.guild.id}","r")
    file_text=file.read()
    file.seek(0)
    lines=file.readlines()
    file.close()

    for user in lines :
        user_info=user.split(',')
        if user_info[2]==str(reuser.id):
            level=int(user_info[4])
            moa=int(user_info[3])


    if level<=1 :
        await ctx.author.send(f"의문의 물건이 +1이거나 가지고 있지 않습니다.")
        return
    
    pricebuy,pricesell=get_price(level)

    file_text=file_text.replace(f"{reuser.id},{'%010d'%moa},{level}",f"{reuser.id},{'%010d'%(moa+pricesell)},0")

    file=open(f"user_info{message.guild.id}","w")
    file.write(file_text)
    file.close()

    writetext=""
    file=open("forcestore","r")
    fileline=file.readlines()
    file.seek(0)
    filetext=file.read()
    file.close()

    for line in fileline : 
        data=line.split(',')
        if data[0]==str(level):
            filetext=filetext.replace(f"{data[0]},{data[1]}",f"{data[0]},{int(data[1])+1}")


    file=open("forcestore","w")
    file.write(filetext)
    file.close()

    file.close()
    
    await ctx.send(f"의문의 물건 +{level}이 판매되었습니다.")
    
def get_price(level) :
    temp=[0,0,0,0]
    temp_buy=0
    temp_sell=0
    for i in range(level) :
        if i<4 :
            temp[i]=i+1
            temp_sell=i+1
        else :
            temp_sell=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp_sell
    for i in range(level) :
        if i<4 :
            temp[i]=i+2
            temp_buy=i+2
        else :
            temp_buy=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp_buy
    return temp_buy,temp_sell




@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 가입(ctx,nickname=None) : 
    if nickname==None:
        await ctx.send("닉네임을 입력해주세요.")
        return
    userdiscordid=[]
    nicks=[]
    file=open(f"user_info{ctx.guild.id}","a+")
    file.seek(0)
    lines=file.readlines()
    for line in lines:
        user=line.split(',')
        userdiscordid.append(user[2])
        nicks.append(user[1].lower())
    if str(ctx.author.id) in userdiscordid :
        await ctx.send("이미 가입하였습니다.")
        return
    if str(nickname).lower() in nicks :
        await ctx.send("중복되는 닉네임이 있습니다.")
        return
    string_pool=string.ascii_letters+string.digits
    result1=""
    for i in range(20) : 
        result1=result1+random.choice(string_pool)
    file.write(f"{result1},{nickname},{ctx.author.id},{'%010d'%20000},0,\n")
    await ctx.send("가입 성공!")
    file.close()


@bot.command()
async def 자산(ctx,nickname=None) : 
    if nickname==None:
        await ctx.send("닉네임을 입력해주세요.")
        return
    file=open(f"user_info{ctx.guild.id}","r")
    lines=file.readlines()
    money=-2000
    for line in lines :
        user=line.split(',')
        if user[1].lower()==str(nickname).lower() :
            money=user[3]
    if money==-2000:
        await ctx.send(f"존재하지 않는 유저입니다.")
    else :
        await ctx.send(f"{nickname}의 자산은 {int(money)}모아입니다.")
    file.close()



def get_chance_multiple(mode) :
    if mode==1 : 
        chance=80
        multiple=1.2
    elif mode==2 : 
        chance=64
        multiple=1.6
    elif mode==3 : 
        chance=48
        multiple=2.2
    elif mode==4 : 
        chance=32
        multiple=3
    elif mode==5 : 
        chance=16
        multiple=4
    elif mode==6 :
        chance=60
        multiple=2
           
    return chance,multiple


@bot.command()
async def 버전(ctx) :
    await ctx.send(version)

@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 베팅(ctx,mode=None,moa=None) :
    try :
        success=True
        file=open(f"user_info{ctx.guild.id}","r")
        lines=file.readlines()
        file.seek(0)
        file_text=file.read()
        money=0
        nickname=""
        for line in lines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                money=int(user[3])
                nickname=user[1]
        file.close()
        
        if money<=0:
            raise Exception('베팅할 돈이 없습니다.')
        if mode==None : 
            raise Exception("모드를 입력해주세요.")
        if int(mode)==6 and moa!=None:
            raise Exception("올인모드는 모아를 입력할수 없습니다.")
        if int(mode)==6 :
            moa=money

        if moa==None :  
            raise Exception("모아를 입력해주세요.")
        if money<int(moa) or int(moa)<0 : 
            raise Exception("보유량보다 많거나 0원 미만으로 베팅하실 수 없습니다.")
        if int(mode)>6 or int(mode)<1 : 
            raise Exception('모드를 잘못 입력했습니다.')
    except Exception as e:
        await ctx.send(f"{e}\n$베팅 (모드) (모아)\n(모드 종류 : 1 80% 1.2배, 2 64% 1.6배, 3 48% 2.2배, 4 32% 3배, 5 16% 4배, 6 60% 2배(올인만 가능)")
        return
    chance,multiple=get_chance_multiple(int(mode))
    result=random.randrange(0,100)
    lose=int(moa)
    end=0
    if result<chance : 
        profit=math.floor(multiple*int(moa))
        end=money-lose+profit
        await ctx.send(f"{nickname} 베팅 성공!")
        success=True
    else :
        end=money-int(moa)
        await ctx.send(f"{nickname} 베팅 실패!")
        save2=random.randrange(0,100)
        success=False
        if save2<10 :
            end+=math.floor(int(moa)*0.3)
            await ctx.send("건 돈의 30% 지급")
    file=open(f"user_info{ctx.guild.id}","w")
    file_text=file_text.replace(f"{ctx.author.id},{'%010d'%money}",f"{ctx.author.id},{'%010d'%end}")
    file.write(file_text)
    file.close()

    if not success :
        await setluckypang(math.floor(int(moa)*0.1),ctx)



@bot.command()
async def 모두(ctx) :
    file=open(f"user_info{ctx.guild.id}","r")
    lines=file.readlines()
    file.close()

    showtext="```"

    for line in lines :
        user=line.split(',')
        showtext+=f"{user[1]} {int(user[3])}\n"
    showtext+="```"
    await ctx.send(showtext)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.default)
async def 일시정지(ctx,reason=None) :
    global cancommand
    if ctx.author.id==382938103435886592 :
        cancommand=not cancommand
        if cancommand : 
            await ctx.send("명령어 사용이 가능합니다.")
        else :
            await ctx.send(f"명령어 사용이 불가능합니다. 이유: {reason}")

#region 복권
@commands.cooldown(1, Lottocool, commands.BucketType.user)
@bot.command()
async def 복권(ctx,amount=1) :
    global canLotto
    global Lottomax
    global lottoRange
    showtext="```"
    if not canLotto :
        await ctx.send("마감되었습니다.")
        return
    nickname=""
    filename=f"user_info{ctx.guild.id}"
    if int(amount)>Lottomax:
        await ctx.send(f"한번에 {Lottomax}개까지 구매 가능합니다.")
        return
    for num in range(int(amount)) :
        i=0
        number=[0,0,0,0]
        num=0
        file=open(filename,"r")
        file_text=file.read()
        file.seek(0)
        lines=file.readlines()
        userid=[]
        for line in lines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                nickname=user[1]
                if int(user[3])<1000:
                    await ctx.send("복권을 살 돈이 부족합니다.(1000모아)")
                    return
                else :
                    file_text=file_text.replace(f"{user[2]},{user[3]}",f"{user[2]},{'%010d'%(int(user[3])-1000)}")
            userid.append(user[2])
        if not str(ctx.author.id) in userid :
            await ctx.send("가입을 해주세요.")
            return
        while i<4 : 
            num=random.randint(1,lottoRange)
            if not num in number :
                number[i]=num
                i+=1
        number.sort()
        number.append(random.choice(number))
        showtext+=nickname+"   "+str(number)+"\n"
        writetext=""
        for num in number :
            writetext+=str(num)+","
        writetext+=str(ctx.author.id)+",\n"
        file=open(f"lotto_{ctx.guild.id}","a")
        file.write(writetext)
        file.close()
        file=open(f"user_info{ctx.guild.id}","w")
        file.write(file_text)
        file.close()
    showtext+="```"
    await ctx.send(showtext)
    await CheckLotto(f"lotto_{ctx.guild.id}",ctx)

async def CheckLotto(filename,ctx) :
    global canLotto
    global Lottocool
    winner=[[],[],[],[]]

    file=open(filename,"r")
    lines=file.readlines()
    await ctx.send(f"{len(lines)}/{Lottocool}")
    showtext="```"
    if len(lines)>=Lottocool :
        canLotto=False
        result=[0,0,0,0]
        special=0
        totalSell=float(len(lines)*1000)
        i=0

        #region 로또 추첨
        while i<4 : 
            num=random.randint(1,lottoRange)
            if not num in result :
                result[i]=num
                i+=1
        result.sort()
        special=random.choice(result)
        #endregion
    
        showtext+=f"당첨 번호 : {result[0]},{result[1]},{result[2]},{result[3]},{special}\n"
        for line in lines :
            nickname=""
            submit=line.split(',')
            i=0
            correct=0
            place=0
            getprice=0
            while i<4:
                if int(submit[i]) in result :
                    correct+=1
                i+=1
            if correct>0:
                if correct==4 :
                    if special==int(submit[4]):
                        place=1
                        getprice=math.floor(totalSell*5)
                        winner[3].append(submit[4])
                    else :
                        place=2
                        getprice=math.floor(totalSell*0.7)
                        winner[2].append(submit[4])
                elif correct==3:
                    place=3
                    getprice=math.floor(totalSell*0.15)
                    winner[1].append(submit[4])
                elif correct==2:
                    place=4
                    getprice=math.floor(totalSell*0.05)
                    winner[0].append(submit[4])

            userfile=open(f"user_info{ctx.guild.id}","r")
            file_text=userfile.read()
            userfile.seek(0)
            userdata=userfile.readlines()
            file.close()
            for sub in userdata :
                cuser=sub.split(',')               
                if submit[5]==cuser[2]:
                    nickname=cuser[1]
                    print(f"{cuser[2]},{'%010d'%(int(cuser[3]))}")
                    print(f"{cuser[2]},{'%010d'%(int(cuser[3])+getprice)}")
                    file_text=file_text.replace(f"{cuser[2]},{'%010d'%(int(cuser[3]))}",f"{cuser[2]},{'%010d'%(int(cuser[3])+getprice)}")
            file=open(f"user_info{ctx.guild.id}","w")
            file.write(file_text)
            file.close()
            if place!=0:
                showtext+=f"{nickname} {place}등 당첨! {getprice}모아 지급! [{submit[0]},{submit[1]},{submit[2]},{submit[3]},{submit[4]}]\n"
        showtext+="```"
        await ctx.send(showtext)
        os.remove(filename)
        canLotto=True
        Lottocool=random.randint(10,30)
            

    
            
@commands.cooldown(1, 0.5, commands.BucketType.default)
@bot.command()
async def 복권확인(ctx) :
    showtext="```"
    file=open(f"lotto_{ctx.guild.id}","r")
    lines=file.readlines()
    for line in lines:
        user=line.split(',')
        if user[4]==str(ctx.author.id):
            showtext+=f"{user[0]},{user[1]},{user[2]},{user[3]}\n"
    showtext+="```"
    await ctx.send(showtext)
            
#endregion   
    
@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 기부(ctx,nickname=None,moa=None) :
    try :
        if nickname==None:
            raise Exception('기부할 닉네임을 입력해주세요.')
            
        if moa==None:
            raise Exception('모아를 입력해주세요.')
        
        if int(moa)<=0 : 
            raise Exception('0원이하로 기부할수 없습니다.')

        
        file=open(f"user_info{ctx.guild.id}","r")
        file_text=file.read()
        file.seek(0)
        lines=file.readlines()
        file.close()
        nicknames=[]
        for line in lines:
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                if int(user[3])<int(moa) :
                    raise Exception("자신 보유 자산보다 많이 기부할수 없습니다.")
            nicknames.append(str(user[1]).lower())
        if not str(nickname) in nicknames :
            raise Exception('닉네임을 잘못 입력했습니다.')
        for line in lines:
            user=line.split(',')
            if user[1].lower()==str(nickname).lower() :
                file_text=file_text.replace(f"{user[1]},{user[2]},{user[3]}",f"{user[1]},{user[2]},{'%010d'%(int(user[3])+int(moa))}")
            if user[2]==str(ctx.author.id) :
                file_text=file_text.replace(f"{user[2]},{user[3]}",f"{user[2]},{'%010d'%(int(user[3])-int(moa))}")
        file=open(f"user_info{ctx.guild.id}","w")
        file.write(file_text)
        file.close()
    except Exception as e :
        await ctx.send(f"{e}\n$기부 (닉네임) (기부할 돈)")
        return
    

    


@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 도움말(ctx,keyword=None) :
    if keyword==None:
        await ctx.send("도움말 (명령어) : 가입, 자산, 베팅, 기부, 복권, 강화")
    elif keyword=="베팅":
        await ctx.send("$베팅 (모드) (돈)\n모드 종류 : 1 80% 1.4배, 2 64% 1.8배, 3 48% 2.2배, 4 32% 2.6배, 5 16% 3배, 6 60% 2배(올인만 가능)")
    elif keyword=="자산":
        await ctx.send("$자산 (닉네임)")
    elif keyword=="복권":
        await ctx.send("$복권 (구매개수 - 기본값 : 1)")
    else :
        await ctx.send("현재 도움말은 베팅,자산, 복권만 지원합니다.")

@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 경제규모(ctx,mode=None,moa=None) :
    sum_money=0
    file=open(f"user_info{ctx.guild.id}","r")
    lines=file.readlines()
    file.close()
    for line in lines :
        user=line.split(',')
        sum_money+=int(user[3])
    await ctx.send(str(sum_money)+"모아")

@bot.command()
async def 닉네임(ctx):
    file=open(f"user_info{ctx.guild.id}","r")
    lines=file.readlines()
    file.close()
    nickname=""
    for line in lines :
        user=line.split(',')
        if int(user[2])==ctx.author.id :
            nickname=user[1]
    await ctx.send(f"{ctx.author.display_name}의 닉네임은 {nickname}입니다.")



@bot.command()
async def 강화(ctx) : 
    global forceMsg
    embed=discord.Embed(title="강화",description="3번 연속 강화 추가!")
    embed.add_field(name="강화 :hammer:",value="강화를 합니다.")
    embed.add_field(name="판매 :grinning:",value="판매를 합니다.")
    embed.add_field(name="강화x3 :fire:",value="강화를 3번 합니다.")
    msg=await ctx.send(embed=embed,content=ctx.author.display_name)
    forceMsg.append(msg.id)
    await msg.add_reaction("🔨")
    await msg.add_reaction("😀")
    await msg.add_reaction("🔥")
    return
    #file=open(f"user_info{ctx.guild.id}","r")

@bot.command()
async def 한강(ctx) : 
    file=open("hanriver.txt","r",encoding="utf-8")
    text=file.read()
    

    url="https://hangang.life/"
    result=requests.get(url = url)
    bs_obj=BeautifulSoup(result.content,"html.parser")
    lf_items=str(bs_obj.find("h1",{"class":"white"}))
    lf_items=re.sub('<.+?>',"",lf_items,0)
    lf_items=re.sub('\n',"",lf_items,0)
    print(lf_items)

    await ctx.send(text+f"\n\n\n현재 한강 수온{lf_items}```")

@commands.cooldown(1, giveMcool, commands.BucketType.user)
@bot.command()
async def 구걸(ctx) :
    file=open(f"user_info{ctx.guild.id}","r")
    file_text=file.read()
    file.seek(0)
    lines=file.readlines()
    file.close()
    userid=[]
    nickname=""
    money=0
    for line in lines :
        user=line.split(',')
        userid.append(user[2])
        if user[2]==str(ctx.author.id) :
            nickname=user[1]
            money=int(user[3])
            if money>0:
                await ctx.send("0모아를 가지고 있어야 구걸할수 있습니다.")
                return
     
    if not str(ctx.author.id) in userid :
        await ctx.send("가입을 해주세요.")
        return


    i=1
    cut=0
    getmoa=0
    result=random.random()*100
    while i<=12:
        cut+=i
        if result<cut:
            getmoa=16000-1000*(i-1)
            break
        else :
            i+=1
    if i==13 :
        getmoa=2500

    print(money+getmoa)
    file_text=file_text.replace(f"{ctx.author.id},{'%010d'%money}",f"{ctx.author.id},{'%010d'%(money+getmoa)}")
    file=open(f"user_info{ctx.guild.id}","w")
    file.write(file_text)
    file.close()
    
    await ctx.send(f"'{nickname}' {getmoa}모아 획득!")


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def 자산이전(ctx,nickname1,nickname2):
    if ctx.author.id!=382938103435886592:
        await ctx.send("제작자 전용 명령어입니다.")
        return
    

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def 강화구매(ctx,level=None):
    try :
        userid=[]
        nickname=""
        money=0
        showtext="```"

        forcefile=open("forcestore","r")
        forcelines=forcefile.readlines()
        forcefile.seek(0)
        forcefile_text=forcefile.read()
        forcefile.close()
        mylevel=0

        userfile=open(f"user_info{ctx.guild.id}","r")
        userfile_text=userfile.read()
        userfile.seek(0)
        userlines=userfile.readlines()
        userfile.close()

        remainlist=[]

        i=0
        while i<29 :
            data=forcelines[i].split(',')
            remainlist.append(int(data[1]))
            i+=1


        if level==None:
            i=0
            while i<29 :
                if remainlist[i]>0 :
                    showtext+=f"의문의 물건 +{i+1}, {remainlist[i]}개 남음,{get_price(i+1)[0]}모아\n"
                i+=1
            
            showtext+='```'
            await ctx.send(showtext)
            return

        level=int(level)
        

        for line in userlines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                nickname=user[1]
                mylevel=int(user[4])
                money=int(user[3])
            userid.append(user[2])

        if not str(ctx.author.id) in userid :
            await ctx.send("가입을 해주세요.")
            return

        if mylevel>0:
            await ctx.send("의문의 물건은 1개만 보유할수 있습니다.")
            return
        
        if level>30 : 
            await ctx.send("의문의 물건은 1~29강만 구매할 수 있습니다.")
            return

        print(remainlist)
        if remainlist[level-1]<=0:
            await ctx.send(f"의문의 물건 +{level}의 매물이 없습니다.")
            return

        for user in userlines :
            userdata=user.split(',')
            if str(ctx.author.id)==userdata[2]:
                if int(userdata[3])>=get_price(level)[0] :
                    userfile_text=userfile_text.replace(f"{userdata[2]},{userdata[3]},0",f"{userdata[2]},{'%010d'%(int(userdata[3])-get_price(level)[0])},{level}")
                else :
                    await ctx.send(f"{get_price(level)[1]-int(userdata[3])}모아가 부족합니다.")
                    return
        
        file=open(f"user_info{ctx.guild.id}","w")
        file.write(userfile_text)
        file.close()
        forcefile_text.replace(f"{level},{remainlist[level-1]}",f"{level},{remainlist[level-1]-1}")

        
        writetext=""
        i=0
        while i<29 :
            if i+1==level:
                writetext+=f"{i+1},{remainlist[i]-1},\n"
            else :
                writetext+=f"{i+1},{remainlist[i]},\n"
            i+=1
        file=open(f"forcestore","w")
        file.write(writetext)
        file.close()

        await ctx.send(f"{nickname}, 의문의 물건 +{level} 구매 성공")

        
        

    except Exception as e :
        await ctx.send(f"{e}\n$강화구매 (레벨)")
    

async def setluckypang(price,ctx):
    global maxlucky
    file=open("luckypang","r")
    stack=int(file.read())
    file.close()

    
    await ctx.send(f"{stack+price}/{maxlucky}")

    if stack+price>=maxlucky:
        nicknames=[]
        moneys=[]
        discordid=[]
        money=0
        userid=0

        userfile=open(f"user_info{ctx.guild.id}","r")
        file_text=userfile.read()
        userfile.seek(0)
        userlines=userfile.readlines()
        userfile.close()
        for user in userlines:
            userinfo=user.split(',')
            nicknames.append(userinfo[1])
            discordid.append(userinfo[2])
            moneys.append(userinfo[3])
        
        
    
        nickname=random.choice(nicknames)
        money=int(moneys[nicknames.index(nickname)])
        userid=discordid[nicknames.index(nickname)]

        print(f"{userid},{'%010d'%(money)}")
        print(f"{userid},{'%010d'%(money+stack+price)}")
        file_text=file_text.replace(f"{userid},{'%010d'%(money)}",f"{userid},{'%010d'%(money+stack+price)}")
        editfile=open(f"user_info{ctx.guild.id}","w")
        editfile.write(file_text)
        editfile.close()
        editfile=open(f"luckypang","w")
        editfile.write(str(0))
        editfile.close()

        await ctx.send(f"{nickname} 럭키팡 당첨! {stack+price}모아 지급!")
    else :
        editfile=open(f"luckypang","w")
        editfile.write(str(stack+price))
        editfile.close()
        
        


            




bot.run(token)