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
token = "NzY4MjgzMjcyOTQ5Mzk5NjEy.X4-Njg.NfyDMPVlLmgLAf8LkX9p0s04QDY"
test_token="NzY4MzcyMDU3NDE0NTY1OTA4.X4_gPg.fg2sLq5F1ZJr9EwIgA_hiVHtfjQ"
version="V1.0.5.1"


@bot.event
async def on_message(message) :
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'{version} $도움말'))



@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 가입(ctx,nickname=None) : 
    if nickname==None:
        await ctx.send("닉네임을 입력해주세요.")
        return
    userdiscordid=[]
    nicks=[]
    file=open(f"user_info{ctx.guild.id}.txt","a+")
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
    file.write(f"{result1},{nickname},{ctx.author.id},{'%010d'%10000},0,\n")
    await ctx.send("가입 성공!")
    file.close()


@bot.command()
async def 자산(ctx,nickname=None) : 
    if nickname==None:
        await ctx.send("닉네임을 입력해주세요.")
        return
    file=open(f"user_info{ctx.guild.id}.txt","r")
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

@commands.cooldown(1, 2, commands.BucketType.default)
@bot.command()
async def 베팅(ctx,mode=None,moa=None) :
    try :
        file=open(f"user_info{ctx.guild.id}.txt","r")
        lines=file.readlines()
        file.seek(0)
        file_text=file.read()
        money=0
        for line in lines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                money=int(user[3])
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
    file=open(f"user_info{ctx.guild.id}.txt","w")
    if result<chance : 
        profit=math.floor(multiple*int(moa))
        end=money-lose+profit
        await ctx.send("베팅 성공!")              
    else :
        end=money-int(moa)
        await ctx.send("베팅 실패!")
        save2=random.randrange(0,100)
        if save2<10 :
            end+=math.floor(int(moa)*0.3)
            await ctx.send("건 돈의 30% 지급")
    file_text=file_text.replace(f"{ctx.author.id},{'%010d'%money}",f"{ctx.author.id},{'%010d'%end}")
    file.write(file_text)
    file.close()

@bot.command()
async def 모두(ctx) :
    file=open(f"user_info{ctx.guild.id}.txt","r")
    lines=file.readlines()
    file.close()

    showtext="```"

    for line in lines :
        user=line.split(',')
        showtext+=f"{user[1]} {int(user[3])}\n"
    showtext+="```"
    await ctx.send(showtext)


@commands.cooldown(1, 5, commands.BucketType.default)
@bot.command()
async def 복권(ctx) :
    filename=f"user_info{ctx.guild.id}.txt"
    i=0
    number=[0,0,0]
    num=0
    file=open(filename,"r")
    file_text=file.read()
    file.seek(0)
    lines=file.readlines()
    for line in lines :
        user=line.split(',')
        if user[2]==str(ctx.author.id) :
            if int(user[3])<1000:
                await ctx.send("복권을 살 돈이 부족합니다.(1000모아)")
            else :
                file_text=file_text.replace(f"{user[2]},{user[3]}",f"{user[2]},{int(user[3])-1000}")
    while i<3 : 
        num=random.randint(1,6)
        if not num in number :
            number[i]=num
            i+=1
    number.sort()
    number.append(random.choice(number))
    writetext=""
    for num in number :
        writetext+=str(num)+","
    writetext+=str(ctx.author.id)+",\n"
    file=open(f"lotto_{ctx.guild.id}.txt","a")
    file.write(writetext)
    file.close()
    file=open(f"user_info{ctx.guild.id}.txt","w")
    file.write(file_text)
    file.close()
    await CheckLotto(f"lotto_{ctx.guild.id}.txt",ctx)


async def CheckLotto(filename,ctx) :
    file=open(filename,"r")
    lines=file.readlines()
    if len(lines)>=10 :
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


        for line in lines :
            submit=line.split(',')
            i=0
            correct=0
            place=0
            getprice=0
            while i<3:
                if result[i]==int(submit[i]) :
                    correct+=1
                i+=1
            
            if correct==3 :
                if special==int(submit[3]):
                    place=1
                    getprice=math.floor(totalSell*1.2)
                else :
                    place=2
                    getprice=math.floor(totalSell*0.3)
            elif correct==2:
                place=3
                getprice=math.floor(totalSell*0.2)
            elif correct==1:
                place=4
                getprice=math.floor(totalSell*0.1)

            file=open(f"user_info{ctx.guild.id}.txt","r")
            file_text=file.read()
            file.seek(0)
            lines=file.readlines()
            file.close()
            for line in lines :
                user=line.split(',')
                file_text=file_text.replace(f"{submit[4]},{user[3]}",f"{submit[4]},{int(user[3])+getprice}")
            file=open(f"user_info{ctx.guild.id}.txt","w")
            file.write(file_text)
            file.close()
            if place!=0:
                user=bot.get_user(int(submit[4]))
                await user.send(f"{place}등 당첨! {getprice}모아 지급!")
        os.remove(filename)
            

    
            



        
    
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

        
        file=open(f"user_info{ctx.guild.id}.txt","r")
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
        file=open(f"user_info{ctx.guild.id}.txt","w")
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
    file=open(f"user_info{ctx.guild.id}.txt","r")
    lines=file.readlines()
    file.close()
    for line in lines :
        user=line.split(',')
        sum_money+=int(user[3])
    await ctx.send(str(sum_money)+"모아")

@bot.command()
async def 닉네임(ctx):
    file=open(f"user_info{ctx.guild.id}.txt","r")
    lines=file.readlines()
    file.close()
    nickname=""
    for line in lines :
        user=line.split(',')
        if int(user[2])==ctx.author.id :
            nickname=user[1]
    await ctx.send(f"{ctx.author.display_name}의 닉네임은 {nickname}입니다.")
    

bot.run(token)