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
import csv
import re
import shutil
import sys
import glob
from reinforce import doforce,sellforce,buyforce
from financial import givemoney,setluckypang
import reinforce
import financial
import seasonmanage
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

token=""
version="V1.1.5.2"
cancommand=True
canLotto=True
getnotice=False

testint=0
testmode=False

if testint==0:
    testmode=False
else :
    testmode=True

Lottocool=0
Lottomax=3

forceMsg=[]
boxMsg=[]

if testmode :
    giveMcool=1 
    Lottocool=1
    token="NzY4MzcyMDU3NDE0NTY1OTA4.X4_gPg.fg2sLq5F1ZJr9EwIgA_hiVHtfjQ"
    version+=" TEST"
    maxlucky=7901
    Lottomax=10
else :
    giveMcool=90
    Lottocool=16
    Lottomax=3
    token = "NzY4MjgzMjcyOTQ5Mzk5NjEy.X4-Njg.NfyDMPVlLmgLAf8LkX9p0s04QDY"
    maxlucky=10000000

   


getPercent={"복권 1개":35,"복권 3개":26,"복권 5개":16,"복권 7개":10,"복권 10개":6,"복권 20개":3,"성공시 4렙업":1,"파괴방지":1.9,"강화비용면제":1,"확정1업":0.1}


seasoncheck=seasonmanage.seasoncheck()
ispreseason=False
if seasoncheck[0]=="false":
    print(f"is not preseason current season is 'season{seasoncheck[1]}'")
    ispreseason=False
elif seasoncheck[0]=="true" :
    print("is preseason")
    ispreseason=True
else :
    print("error")
    sys.exit()

lottoRange=0

    




@bot.event
async def on_message(tempmessage) :
    global getnotice
    if tempmessage.author.id!=768283272949399612 and tempmessage.channel.id==771203131836989443 and tempmessage.author.id!=768372057414565908 :
        if len(tempmessage.content)>50 :    
            await tempmessage.delete()

    if str(tempmessage.content).startswith('$') :
        if cancommand :
            if tempmessage.channel.id!=771203131836989443 and tempmessage.channel.id!=709647685417697372 and tempmessage.channel.id!=775626447854764063:
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
                        channel=bot.get_channel(771203131836989443)
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
    channel=bot.get_channel(771203131836989443)
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
    global boxMsg
    global maxlucky
    global ispreseason
    if user.bot :
        return

    if reaction.message.id in boxMsg :
        if user.display_name==reaction.message.content :
            if str(reaction.emoji)=="🎁" or str(reaction.emoji)=="❌" or str(reaction.emoji)=="👜" : 
                await reaction.message.delete()
            if str(reaction.emoji)=="🎁":
                await BuyBox(reaction.message,user)
                boxMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="❌":
                boxMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="👜":
                await CheckItem(reaction.message,user)
                boxMsg.remove(reaction.message.id)
    
    if reaction.message.id in forceMsg :
        if user.display_name==reaction.message.content :
            if str(reaction.emoji)=="🔥" or str(reaction.emoji)=="😀" or str(reaction.emoji)=="🔨" or str(reaction.emoji)=="🛡️" or str(reaction.emoji)=="⏩" or str(reaction.emoji)=="⭐" : 
                await reaction.message.delete()
            if str(reaction.emoji)=="🔨":
                await doforce(reaction.message,user,1,ispreseason,maxlucky)
                forceMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="😀":
                ispreseason=await sellforce(reaction.message,user)
                forceMsg.remove(reaction.message.id)
                if ispreseason:
                    ispreseason=True
            elif str(reaction.emoji)=="🔥":
                await doforce(reaction.message,user,3,ispreseason,maxlucky)
                forceMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="🛡️":
                await doforce(reaction.message,user,2,ispreseason,maxlucky)
                forceMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="⏩":
                await doforce(reaction.message,user,4,ispreseason,maxlucky)
                forceMsg.remove(reaction.message.id)
            elif str(reaction.emoji)=="⭐":
                await doforce(reaction.message,user,5,ispreseason,maxlucky)
                forceMsg.remove(reaction.message.id)

            
            







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
    userid=0
    user=None
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
            userid=int(user[2])
    user=ctx.guild.get_member(userid)

    if money==-2000:
        await ctx.send(f"존재하지 않는 유저입니다.")
    else :
        await ctx.send(f"{nickname}({user.display_name})의 자산은 {int(money)}모아입니다.")
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
    await ctx.send(f"모아봇 버전 : {version}\n강화 : {reinforce.version}\n재산 : {financial.version}")

@bot.command()
async def 시즌(ctx) :
    if not ispreseason:
        await ctx.send(f"season{seasoncheck[1]}")
    else :
        await ctx.send(f"preseason")


@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 베팅(ctx,mode=None,moa=10000) :
    global maxlucky
    try :
        bonusback=0
        success=True
        file=open(f"user_info{ctx.guild.id}","r")
        lines=file.readlines()
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
        
        if int(mode)==6 :
            if moa==10000:
                moa=math.floor(money*0.5)
            else :
                await ctx.send("베팅 6은 보유액의 절반만 가능합니다.")
                return

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
    profit=0
    if result<chance : 
        profit=math.floor(multiple*int(moa))
        await ctx.send(f"{nickname} 베팅 성공!")
        success=True
    else :
        await ctx.send(f"{nickname} 베팅 실패!")
        save2=random.randrange(0,100)
        success=False
        if save2<10 :
            bonusback=math.floor(lose*0.3)
            await ctx.send("건 돈의 30% 지급")
    
    
    givemoney(ctx,nickname,profit-lose+bonusback)


    if not success :
        await setluckypang(math.floor(int(moa)*0.1),ctx,maxlucky)



@bot.command()
async def 모두(ctx) :
    try :
        file=open(f"user_info{ctx.guild.id}","r")
        lines=file.readlines()
        file.close()
        userlist={}
        showtext="```"

        for line in lines :
            user=line.split(',')
            userlist[user[1]]=int(user[3])
            print(userlist)


        for key,value in userlist.items():
            rank=1
            for userhave in userlist.values():
                if value<userhave:
                    rank+=1
            showtext+=f"{key} {value} {rank}위\n"
        showtext+="```"
        await ctx.send(showtext)
            
    except Exception as e :
        await ctx.send(f"{e}\n가입한 사람이 없습니다.")

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
    try:
        if not canLotto :
            await ctx.send("마감되었습니다.")
            return
        amount=int(amount)
        await BuyLotto(ctx,amount,False)
    except Exception as e:
        await ctx.send(f"복권 (수량)\n{e}")

async def CheckLotto(filename,ctx) :
    global canLotto
    global Lottocool

    if ispreseason: 
        lottoRange=8
    else :
        lottoRange=10

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
                        getprice=5000000
                    else :
                        place=2
                        getprice=1000000
                elif correct==3:
                    place=3
                    getprice=5000
                elif correct==2:
                    place=4
                    getprice=1000

            userfile=open(f"user_info{ctx.guild.id}","r")
            userdata=userfile.readlines()
            file.close()
            for sub in userdata :
                cuser=sub.split(',')               
                if submit[5]==cuser[2]:
                    nickname=cuser[1]
                    givemoney(ctx,nickname,getprice)

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

async def BuyLotto(ctx,amount,FromBox=False):
    global Lottomax
    global lottoRange
    if ispreseason: 
        lottoRange=8
    else :
        lottoRange=10
    showtext="```"
    nickname=""
    filename=f"user_info{ctx.guild.id}"
    if int(amount)>Lottomax and not FromBox:
        await ctx.send(f"한번에 {Lottomax}개까지 구매 가능합니다.")
        return
    for num in range(amount) :
        i=0
        number=[0,0,0,0]
        num=0
        file=open(filename,"r")
        lines=file.readlines()
        userid=[]
        for line in lines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                nickname=user[1]
                if not FromBox:
                    if int(user[3])<1000:
                        await ctx.send("복권을 살 돈이 부족합니다.(1000모아)")
                        return
                    else :
                        givemoney(ctx,nickname,-1000)
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
        
    showtext+="```"
    await ctx.send(showtext)
    await CheckLotto(f"lotto_{ctx.guild.id}",ctx)

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
        
        #파일 읽어서 기부하는 사람의 닉네임, 기부받는 사람의 닉네임 받아들이기
        givenickname=""
        receivenickname=str(nickname).lower()


        file=open(f"user_info{ctx.guild.id}","r")
        file.seek(0)
        lines=file.readlines()
        file.close()
        for line in lines:
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                givenickname=user[1]
                if int(user[3])<int(moa) :
                    raise Exception("자신 보유 자산보다 많이 기부할수 없습니다.")
        
        #기부 하는 사람이랑 기부 받는 사람이랑 닉네임 같으면 기부불가
        if receivenickname==givenickname:
            raise Exception('자신에게 기부할수 없습니다.')

        #givemoney 2개 함수로 돈 조절
        check=givemoney(ctx,receivenickname,int(moa))

        if check==0:
            await ctx.send("존재하지 않는 유저입니다.")
            return

        givemoney(ctx,givenickname,-int(moa))



        #기부 완료 메세지 보내기
        await ctx.send(f"{givenickname}, {receivenickname}에게 {moa}모아 기부완료")


        
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
    countUser=0
    for line in lines :
        user=line.split(',')
        sum_money+=int(user[3])
        countUser+=1

    sendtext=f"총 경제규모 : {sum_money}모아\n1인당 경제규모 : {'%.3f'%(sum_money/countUser)}모아"
    await ctx.send(sendtext)

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
    embed=discord.Embed(title="강화",description="14억을 가지고 있다면 31>32 성공확률 100%")
    embed.add_field(name="강화 :hammer:",value="강화를 합니다.")
    embed.add_field(name="판매 :grinning:",value="판매를 합니다.")
    embed.add_field(name="강화x3 :fire:",value="강화를 3번 합니다.")
    embed.add_field(name="파괴방지 강화 :shield:",value="파괴방지 후 강화를 합니다.(비용 1.1배)")
    embed.add_field(name="4렙업 :fast_forward:",value="성공시 4렙, 크리티컬 성공시 6렙을 올립니다.(비용 2배)")
    embed.add_field(name="확정1업 :star:",value="100% 확률로 업그레이드에 성공합니다. 단, 크리티컬 성공 확률이 없습니다.(비용 20배)")
    msg=await ctx.send(embed=embed,content=ctx.author.display_name)
    forceMsg.append(msg.id)
    emojilist=["🔨","😀","🔥","🛡️","⏩","⭐"]
    for emoji in emojilist :
        if msg:
            await msg.add_reaction(emoji)

    return



@bot.command()
async def 상자구매(ctx) : 
    global boxMsg
    embed=discord.Embed(title="상자구매",description="")
    embed.add_field(name="강화 관련 아이템 랜덤 박스 :gift:",value="6000모아")
    embed.add_field(name="구매 안함 :x:",value="구매를 하지 않습니다.")
    embed.add_field(name="보유 확인 :handbag:",value="보유 현황을 확인합니다.")
    msg=await ctx.send(embed=embed,content=ctx.author.display_name)
    boxMsg.append(msg.id)
    await msg.add_reaction("🎁")
    await msg.add_reaction("❌")
    await msg.add_reaction("👜")
    return

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
            break
     


    

    getmoa=financial.GetBeggingMoa()

    if ispreseason:
        getmoa*=3

    check=givemoney(ctx,nickname,getmoa)

    if check==0:
        await ctx.send("가입을 해주세요.")
        return

    
    await ctx.send(f"'{nickname}', {getmoa}모아 획득!")


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def 자산이전(ctx,nickname1,nickname2,moa):
    if ctx.author.id!=382938103435886592:
        await ctx.send("제작자 전용 명령어입니다.")
        return

    check=[]
    moa=int(moa)
    check.append(givemoney(ctx,nickname1,moa))
    check.append(givemoney(ctx,nickname2,moa))

    if 0 in check :
        await ctx.send("존재하지 않는 유저입니다.")
        return

    await ctx.send(f"{nickname1}의 {moa}모아를 {nickname2}에게 이전 완료")
    

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def 강화구매(ctx,level=None):
    await buyforce(ctx,level)


async def BuyBox(message,reuser):
    haveitem={}
    ctx=message.channel

    print(sum(getPercent.values()))

    if sum(getPercent.values())!=100:
        return

    get=""
    count=1
    writetext=""
    
    if os.path.isfile(f"forceitem{reuser.id}"):
        file=open(f"forceitem{reuser.id}","r")
        lines=file.readlines()
        for line in lines :
            have=line.split(':')
            haveitem[have[0]]=int(have[1])
            print(haveitem)
    else:
        file=open(f"forceitem{reuser.id}","w")
        file.close()


    #region 반복 구간 시작

    for i in range(count):
        file=open(f"user_info{message.guild.id}","r")
        lines=file.readlines()
        file.close()
        userindex=0

        
        index=0
        for user in lines :
            user_info=user.split(',')
            if user_info[2]==str(reuser.id):
                moa=int(user_info[3])
                nickname=user_info[1]
                userindex=index
            index+=1
        
        need=6000

        if need>moa :
            await ctx.send(f"{need-moa}모아가 부족합니다.")
            break
        else:
            lines[userindex]=lines[userindex].replace(f"{reuser.id},{'%010d'%moa}",f"{reuser.id},{'%010d'%(moa-need)}")
            writetext+=""
            for line in lines :
                writetext+=line
            file=open(f"user_info{message.guild.id}","w")
            file.write(writetext)
            file.close()

        result=random.random()*100

        print(result)

        cut=0
        keys=getPercent.keys()
        print(get)
        print(keys)
        for percentkey in keys :
           cut+=getPercent[percentkey]

           if result<cut:
               get=percentkey
               break

 
        
        if get in haveitem.keys() :
            # 보유정보 +1하기
            haveitem[get]+=1
        else :
            #보유정보 1로 추가
            haveitem[get]=1

        writetext=""
        for key,value in haveitem.items():
            writetext+=f"{key}:{value}:\n"
            print(writetext)

        file=open(f"forceitem{reuser.id}","w")
        file.write(writetext)
        file.close()

        await ctx.send(f"{nickname}, '{get}'획득!")
        await setluckypang(need,ctx,maxlucky)
    #endregion
            


async def CheckItem(message,reuser):    
    file=open(f"forceitem{reuser.id}","r")
    file_text=file.read()
    file.close()
    await message.channel.send('```'+file_text+'```')


@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 아이템사용(ctx,itemname=None):
    if itemname==None:
        await ctx.send("사용할 아이템 이름을 입력해주세요.")
        return

    itemlist=getPercent.keys()
    itemhave={}
    itemfile=open(f"forceitem{ctx.author.id}","r")
    itemlines=itemfile.readlines()
    itemfile.close()

    useitem=""
    gethave=0
    for line in itemlines :
        info=line.split(':')
        itemhave[info[0]]=int(info[1])

    if itemname in itemlist:
        useitem=itemname
        if itemname in itemhave.keys():
            itemhave[itemname]-=1
        else :
            await ctx.send("가지고 있지 않는 아이템입니다.")
    else:
        await ctx.send("아이템 이름을 잘못입력했습니다.")
        return


    if itemhave[itemname]<=0:
        itemhave.pop(itemname)
        print(itemhave)

    writetext=""
    for key,value in itemhave.items():
        writetext+=f"{key}:{value}:\n"
    itemfile=open(f"forceitem{ctx.author.id}","w")
    itemfile.write(writetext)
    itemfile.close()


    if str(useitem).startswith("복권"):
        intfind=re.findall("\d+",useitem)
        await BuyLotto(ctx,int(intfind[0]),True)
        itemfile.close()
        return
    elif str(useitem)=="성공시 4렙업":
        await doforce(ctx,ctx.author,4,ispreseason,maxlucky,True)
    else :
        await ctx.send("아이템 사용은 복권 교환권과 '성공시 4렙업'만 가능합니다.")

@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 아이템구매(ctx,itemno=None):
    itemhave={}
    writetext=""
    #상자 구매 이력이 없으면 파일 생성
    if not os.path.isfile(f"forceitem{ctx.author.id}"):
        file=open(f"forceitem{ctx.author.id}","w")
        file.close()
    else :
        file=open(f"forceitem{ctx.author.id}","r")
        fileline=file.readlines()
        for line in fileline :
            info=line.split(':')
            itemhave[info[0]]=int(info[1])

    showtext='```'
    tradefile = open('trade.csv', 'r')
    filetextline=tradefile.readlines()
    tradefile.close()
    i=0
    for line in filetextline :
        i+=1
        info=line.split(',')
        showtext+=f"{i} : {info[0]},{info[1]}\n"
    
    showtext+='```'
    if itemno==None:
        await ctx.send(showtext)
    else :
        if int(itemno)<len(filetextline)+1: 
            #filetextline[int(itemno)-1]을 split해서 정보 가져오기
            realinfo=filetextline[int(itemno)-1].split(',')
            buyitem=realinfo[0]
            buyprice=int(realinfo[1])
            owner=realinfo[2]
            ownerhavingmoney=0
            ownernick=""

            buyindex=0
            sellindex=0
            

            #userfile 오픈후 readline으로 정보 가져옴
            userfile=open(f"user_info{ctx.guild.id}","r")
            userfilelines=userfile.readlines()
            userfile.close()
            

            havingmoney=0
            i=0
            #readline으로 가져온 걸로 for문을 돌려 구매자 닉네임과 보유금액, 판매자 닉네임 가져오기
            for user in userfilelines:
                userinfo=user.split(',')
                if userinfo[2]==str(ctx.author.id):
                    havingmoney=int(userinfo[3])
                    buyindex=i
                elif userinfo[2]==owner:
                    ownernick=userinfo[1]
                    sellindex=i
                    ownerhavingmoney=int(userinfo[3])

                i+=1

            
            if owner==str(ctx.author.id):
                await ctx.send("자신이 판매한 물건은 구매할 수 없습니다.")
                return

            #살 돈이 있다면 구매자의 돈을 빼고 그 돈의 10%를 제외한 돈을 판매자에게 지급
            if havingmoney>=buyprice:
                userfilelines[buyindex]=userfilelines[buyindex].replace(f"{ctx.author.id},{'%010d'%havingmoney}",f"{ctx.author.id},{'%010d'%(havingmoney-buyprice)}")
                userfilelines[sellindex]=userfilelines[sellindex].replace(f"{owner},{'%010d'%ownerhavingmoney}",f"{owner},{'%010d'%(ownerhavingmoney+math.floor(buyprice*0.9))}")
            else :
                await ctx.send(f"{buyprice-havingmoney}모아가 부족합니다.")
                return

            writetext=""
            for line in userfilelines:
                writetext+=line
            userfile=open(f"user_info{ctx.guild.id}","w")
            userfile.write(writetext)
            userfile.close()
            
            for line in filetextline:
                writetext+=line

            #userfile 오픈후 파일쓰기
            userfile=open(f"trade.csv","w")
            userfile.write(writetext)
            userfile.close()

            #구매자 아이템 보유 정보 수정
            itemhave[buyitem]+=1
            writetext=""
            for key,value in itemhave.items():
                writetext+=f"{key}:{value}:\n"
                print(writetext)

            file=open(f"forceitem{ctx.author.id}","w")
            file.write(writetext)
            file.close()



            #거래시장 csv 수정
            filetextline.pop(int(itemno)-1)

            writetext=""
            print(filetextline)
            for line in filetextline :
                if line!="" :
                    writetext+=line

            tradefile = open('trade.csv', 'w', newline="")
            tradefile.write(writetext)
            tradefile.close()

            


            #구매, 판매 완료 보내기
            await ctx.send(f"{ownernick}의 {buyitem}을 {buyprice}모아에 구매 완료")

        else :
            return

@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 아이템판매(ctx,itemname=None,price=None):
    try:
        if itemname==None:
            raise Exception("아이템 이름을 입력해주세요.")

        if price==None:
            raise Exception("팔 가격을 입력해주세요.")

        itemlist=[]
        itemhave={}
        itemfile=open(f"forceitem{ctx.author.id}","r")
        itemlines=itemfile.readlines()
        itemfile.close()

        for line in itemlines :
            info=line.split(':')
            itemhave[info[0]]=int(info[1])
            itemlist.append(info[0])



        if itemname in itemhave.keys():
            itemhave[itemname]-=1
            print(itemhave)
            if itemhave[itemname]<=0:
                itemhave.pop(itemname)
                print(itemhave)

        else :
            await ctx.send(f"'{itemname}' 보유하지 않음")
            return

        writetext=""
        for key,value in itemhave.items():
            writetext+=f"{key}:{value}:\n"
        
        itemfile=open(f"forceitem{ctx.author.id}","w")
        itemfile.write(writetext)
        itemfile.close()

        if itemname in itemlist:
            tradefile = open('trade.csv', 'at', newline="")
            writer = csv.writer(tradefile)
            
            writer.writerow([itemname,int(price),ctx.author.id,None])
            tradefile.close()
            await ctx.send(f"{itemname} 아이템이 {price}모아에 올려짐")
        else :
            await ctx.send("존재하지 않는 아이템입니다.")
            return
    except Exception as e :
        await ctx.send(f"{e}\n$아이템판매 '(아이템 이름)' (판매 가격)")

@bot.command()
async def 운영자지급(ctx,nickname,moa) :
    if ctx.author.id!=382938103435886592:
        await ctx.send("권한이 없습니다.")
        return

    check=givemoney(ctx,nickname,moa)

    if check==0:
        await ctx.send("존재하지 않는 유저입니다.")
        return

    

    await ctx.send(f"{nickname}에게 {moa}모아 지급 완료")


print(f"testmode : {testmode}")
print(f"testmode : {testmode}")
print(f"testmode : {testmode}")


time.sleep(10)
bot.run(token)