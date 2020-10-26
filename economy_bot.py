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

bot = commands.Bot(command_prefix='$')

token=""
version="V1.0.7.2"
cancommand=True
canLotto=True
getnotice=False

testmode=False
Lottocool=0
Lottomax=3

if testmode :
    giveMcool=1
    Lottocool=1
    token="NzY4MzcyMDU3NDE0NTY1OTA4.X4_gPg.fg2sLq5F1ZJr9EwIgA_hiVHtfjQ"
    version+=" TEST"
    Lottomax=10
else :
    giveMcool=60
    Lottocool=16
    Lottomax=3
    token = "NzY4MjgzMjcyOTQ5Mzk5NjEy.X4-Njg.NfyDMPVlLmgLAf8LkX9p0s04QDY"
    



@bot.event
async def on_message(tempmessage) :
    global getnotice
    if tempmessage.author.id!=768283272949399612 and tempmessage.channel.id==768343875001516074 and tempmessage.author.id!=768372057414565908 :
        if len(tempmessage.content)>50 :    
            await tempmessage.delete()

    if str(tempmessage.content).startswith('$') :
        if cancommand :
            if tempmessage.channel.id!=768343875001516074 and tempmessage.channel.id!=709647685417697372 :
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


@bot.event
async def on_reaction_add(reaction,user) :
    if user.bot :
        return
    if str(reaction.emoji)=="👏":
        #await singforce(user)
        await reaction.message.channel.send(reaction.message.content)
    if str(reaction.emoji)=="🔨":
        await reaction.message.channel.send(reaction.message.content)


async def singforce(user) : 
    await user.send(user.id)

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
        if i<3 :
            temp[i]=1
            temp2=1
        elif i<6 :
            temp[i]=2
            temp2=2
        else :
            temp2=sum(temp)
            temp[0]=temp[1]
            temp[1]=temp[2]
            temp[2]=temp[3]
            temp[3]=temp[4]
            temp[4]=temp[5]
            temp[5]=temp2
    return temp2

async def doforce(ctx):
    level = 1
    cri_success=0.0
    success=0.0
    not_change=0.0
    fail=0.0
    destroy=0.0
    result=0.0
    change=0


    moa=500
    level=1

    need=get_need(level)
    if need>moa :
        ctx.author.send(f"{need-moa}모아가 부족합니다.")
    if level == 30 :
        await ctx.author.send("이미 의문의 물건 +30을 가지고 있습니다.")
        return
    elif level == 0 :
        await ctx.author.send("의문의 물건을 가지고 있지 않습니다.")
        return

    if level !=29 :
        cri_success=0.05*(30-level)
    else :
        cri_success=0.0

    if level==1 :
        destroy=0.0
    else :
        destroy=0.73*(level-29)+20

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
        sql=f"update user_info set item5=item5+{change},moa=moa-{need} where discorduserid={ctx.author.id}"
        if change>0 :
            await ctx.send(f"강화 레벨 {level}에서 {change} 상승! 현재 레벨 : {level+change}")
        elif change<0 :
            await ctx.send(f"강화 레벨 {level}에서 {-change} 감소! 현재 레벨 : {level+change}")
        else :
            await ctx.send(f"강화 레벨 {level}에서 변동 없음! 현재 레벨 : {level}")      
    else :
        sql=f"update user_info set item5=0,moa=moa-{need} where discorduserid={ctx.author.id}"
        await ctx.send(f"의문의 물건 +{level} 파괴...")
    


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
    file=open(f"user_info{ctx.guild.id}","w")
    if result<chance : 
        profit=math.floor(multiple*int(moa))
        end=money-lose+profit
        await ctx.send(f"{nickname} 베팅 성공!")
    else :
        end=money-int(moa)
        await ctx.send(f"{nickname} 베팅 실패!")
        save2=random.randrange(0,100)
        if save2<10 :
            end+=math.floor(int(moa)*0.3)
            await ctx.send("건 돈의 30% 지급")
    file_text=file_text.replace(f"{ctx.author.id},{'%010d'%money}",f"{ctx.author.id},{'%010d'%end}")
    file.write(file_text)
    file.close()

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
async def 일시정지(ctx) :
    global cancommand
    if ctx.author.id==382938103435886592 :
        cancommand=not cancommand
        if cancommand : 
            await ctx.send("명령어 사용이 가능합니다.")
        else :
            await ctx.send("명령어 사용이 불가능합니다.")

#region 복권
@commands.cooldown(1, Lottocool, commands.BucketType.user)
@bot.command()
async def 복권(ctx,amount=1) :
    global canLotto
    global Lottomax
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
        number=[0,0,0]
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
        while i<3 : 
            num=random.randint(1,6)
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
        result=[0,0,0]
        special=0
        totalSell=float(len(lines)*1000)
        i=0

        #region 로또 추첨
        while i<3 : 
            num=random.randint(1,6)
            if not num in result :
                result[i]=num
                i+=1
        result.sort()
        special=random.choice(result)
        #endregion
    
        showtext+=f"당첨 번호 : {result[0]},{result[1]},{result[2]},{special}\n"
        for line in lines :
            nickname=""
            submit=line.split(',')
            i=0
            correct=0
            place=0
            getprice=0
            while i<3:
                if int(submit[i]) in result :
                    correct+=1
                i+=1
            if correct>0:
                if correct==3 :
                    if special==int(submit[3]):
                        place=1
                        getprice=math.floor(totalSell*1.5)
                        winner[3].append(submit[4])
                    else :
                        place=2
                        getprice=math.floor(totalSell*0.5)
                        winner[2].append(submit[4])
                elif correct==2:
                    place=3
                    getprice=math.floor(totalSell*0.3)
                    winner[1].append(submit[4])
                elif correct==1:
                    place=4
                    getprice=math.floor(totalSell*0.2)
                    winner[0].append(submit[4])

            userfile=open(f"user_info{ctx.guild.id}","r")
            file_text=userfile.read()
            userfile.seek(0)
            userdata=userfile.readlines()
            file.close()
            for sub in userdata :
                cuser=sub.split(',')               
                if submit[4]==cuser[2]:
                    nickname=cuser[1]
                    print(f"{cuser[2]},{'%010d'%(int(cuser[3]))}")
                    print(f"{cuser[2]},{'%010d'%(int(cuser[3])+getprice)}")
                    file_text=file_text.replace(f"{cuser[2]},{'%010d'%(int(cuser[3]))}",f"{cuser[2]},{'%010d'%(int(cuser[3])+getprice)}")
            file=open(f"user_info{ctx.guild.id}","w")
            file.write(file_text)
            file.close()
            if place!=0:
                showtext+=f"{nickname} {place}등 당첨! {getprice}모아 지급! [{submit[0]},{submit[1]},{submit[2]},{submit[3]}]\n"
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
        await ctx.send("도움말 (명령어) : 가입, 자산, 베팅, 기부")
    elif keyword=="베팅":
        await ctx.send("$베팅 (모드) (돈)\n모드 종류 : 1 80% 1.4배, 2 64% 1.8배, 3 48% 2.2배, 4 32% 2.6배, 5 16% 3배, 6 85% 1.13배(올인만 가능)")
    else :
        await ctx.send("현재 도움말은 베팅만 지원합니다.")

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

forceMsg=[]

@bot.command()
async def 강화(ctx) : 
    global forceMsg
    embed=discord.Embed(title="강화",description="준비중입니다.")
    embed.add_field(name="가입 :clap:",value="강화 가입을 합니다.")
    embed.add_field(name="강화 :hammer:",value="강화를 합니다.")
    msg=await ctx.send(embed=embed,content=ctx.author.display_name)
    forceMsg.append(msg)
    await msg.add_reaction("👏")
    await msg.add_reaction("🔨")
    return
    #file=open(f"user_info{ctx.guild.id}","r")
    await ctx.send("준비중입니다.")
    file=open(f"reinforce{ctx.guild.id}","w")
    file_text=file.read()
    lines=file.readlines()

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


     

bot.run(token)