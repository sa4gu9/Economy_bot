import asyncio
import math
import random
import discord
from financial import givemoney,setluckypang
import datetime
import datamanage
import json

version="V1.6"

maxlevel=36

async def doforce(message,reuser,mode,ispreseason,maxlucky,useitem=False):
    
    NotDestroy=False
    FastUp=False
    count=1

    if mode==2:
        NotDestroy=True        
    elif mode==3:
        count=3
    elif mode==4:
        FastUp=True
        
        
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
    totalfailneed=0

    #region 반복 구간 시작

    for i in range(count):
        file=open(f"data/user_info{message.guild.id}","r")
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

        if level>=maxlevel:
            await ctx.send("강화를 완료한 의문의 물건입니다. 판매시 시즌이 종료됩니다.")
            return
        


        cri_success=GetCriSuccess(level)
        

        destroy=GetDestroy(level,ispreseason)

        

        success=GetSuccess(level)
        fail=get_fail(level)

        not_change=100 - cri_success - success - fail - destroy

        if mode==5:
            cri_success=0
            success=95
            not_change=0
            fail=0
            destroy=100-success
            need*=10

        if NotDestroy:
            if destroy!=0:
                if not ispreseason:
                    need=math.floor(need*1.1)
                not_change+=destroy
                destroy=0
            else :
                await ctx.send("파괴 방지가 불가능합니다.")
                return
        if FastUp :
            if level>23:
                await ctx.send("24렙 이상은 4렙 업 찬스를 사용할 수 없습니다.")
                return
            else :
                if not useitem :
                    if ispreseason:
                        need=math.floor(need*2)
                    else :
                        need*=3

        
        if level == 0 :
            await ctx.send("의문의 물건을 가지고 있지 않습니다.")
            break

        if need>moa :
            await ctx.send(f"{need-moa}모아가 부족합니다.")
            break
        
        
        
        result=random.random()*100

        print(result)
        if result<cri_success :
            print(f"{result}  {cri_success}")
            if FastUp:
                change=6
            else :
                change=2        
        elif result<cri_success + success :
            print(f"{result}  {cri_success+success}")
            if FastUp:
                change=4
            else :
                change=1
        elif result<cri_success+success + not_change :
            print(f"{result}  {cri_success+success+ not_change}")
            change=0
        elif result < cri_success + success + not_change + fail :
            print(f"{result}  {cri_success+success+ not_change+ fail}")
            change=-1
        else :
            change=-10
        

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
        
        file=open(f"data/user_info{ctx.guild.id}","w")
        file.write(file_text)
        file.close()

        if change<=0:
            totalfailneed+=math.floor(need*0.1)
        asyncio.sleep(0.1)
    #endregion
    if totalfailneed!=0:
        await setluckypang(math.floor(totalfailneed*0.1),message.channel,maxlucky)

def GetSuccess(level):
    return 100-2.57*level

def GetDestroy(level,ispreseason):
    destroy=0
    if ispreseason:
        destroy=0.0
    else :
        destroy=0.8*(level-1)
    return destroy

def GetCriSuccess(level):
    if level <=29 :
        cri_success=0.05*(30-level)
    else :
        cri_success=0.0
    return cri_success

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

def get_fail(level):
    temp=0
    for i in range(level) :
        if i==0:
            temp=0
        else :
            temp+=0.1*i

    if level%7==0:
        temp=0

    return temp






async def sellforce(message,reuser) :
    ctx=message.channel
    level=0

    file=open(f"data/user_info{message.guild.id}","r")
    file.seek(0)
    lines=file.readlines()
    file.close()

    nickname=""

    for user in lines :
        user_info=user.split(',')
        if user_info[2]==str(reuser.id):
            nickname=user_info[1]
            level=int(user_info[4])


    if level<=1 :
        await reuser.send(f"의문의 물건이 +1이거나 가지고 있지 않습니다.")
        return
    
    pricesell=get_price(level)[1]

    givemoney(ctx,nickname,pricesell,1)

    if level>=maxlevel:
        await ctx.send(f"{maxlevel}강을 판매되어서 시즌이 종료되었습니다. 관련 공지가 있을때까지 프리시즌이 유지됩니다.")

        datamanage.datareset(message.guild)
        
        return True

    forceSale={}
    with open("data/forcestore.json","r") as forceFile :
        forceSale=json.load(forceFile)

    

    if f"{level}" in forceSale.keys():
        forceSale[f"{level}"]+=1
    else :
        forceSale[f"{level}"]=1


    with open("data/forcestore.json","w") as forceFile :
        json.dump(forceSale,forceFile)


    await ctx.send(f"의문의 물건 +{level}이 판매되었습니다.")

def get_price(level) :
    level=int(level)
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

async def buyforce(ctx,level):
    try :
        forceSale={}
        with open("data/forcestore.json","r") as forceFile:
            forceSale=json.load(forceFile)


        
        sale=False
        chour=datetime.datetime.now().time().hour
        if (datetime.datetime.now().weekday()==5 or datetime.datetime.now().weekday()==6) and (chour==13 or chour==21 or chour==17):
            sale=True


        userid=[]
        nickname=""
        showtext="```"

        userfile=open(f"data/user_info{ctx.guild.id}","r")
        userlines=userfile.readlines()
        userfile.close()
        
        if level==None:
            if sale:
                showtext+="의문의 물건 +15이상 20% 할인중!\n"
            for key,value in list(sorted(forceSale.items())):
                showtext+=f"의문의 물건 +{key}, {value}개 남음, {get_price(key)[0]}모아\n"
            showtext+='```'
            await ctx.send(showtext)
            return

        limit=forceSale.get(level)


        for line in userlines :
            user=line.split(',')
            if user[2]==str(ctx.author.id) :
                nickname=user[1]
                mylevel=int(user[4])
            userid.append(user[2])

        if not str(ctx.author.id) in userid :
            await ctx.send("가입을 해주세요.")
            return

        if mylevel>0:
            await ctx.send("의문의 물건은 1개만 보유할수 있습니다.")
            return
        
        if limit<=0:
            await ctx.send(f"의문의 물건 +{level}의 매물이 없습니다.")
            return
        price=0
        if int(level)>=15 and sale :
            price=math.floor(get_price(level)[0]*0.8)
        else :
            price=get_price(level)[0]

        print(price)


        for user in userlines :
            userdata=user.split(',')
            if str(ctx.author.id)==userdata[2]:
                if int(userdata[3])>=price :
                    value=givemoney(ctx,nickname,price,2,level)
                    print(value)
                else :
                    await ctx.send(f"{price-int(userdata[3])}모아가 부족합니다.")
                    return
        
        forceSale[level]-=1

        with open("data/forcestore.json","w") as forceFile:
            json.dump(forceSale,forceFile)

        await ctx.send(f"{nickname}, 의문의 물건 +{level} 구매 성공")

        
        

    except Exception as e :
        await ctx.send(f"{e}\n$강화구매 (레벨)")