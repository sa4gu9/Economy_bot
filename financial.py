import asyncio
import random
import discord

version="V1.2"



def givemoney(ctx,nickname,moa,mode=None,getlevel=None):
    file=open(f"user_info{ctx.guild.id}","r")
    lines=file.readlines()
    file.close()
    nicknames=[]

    writetext=""
    index=0
    getid=0
    gethavemoney=0
    for line in lines :
        user=line.split(',')
        nicknames.append(user[1].lower())
        if user[1].lower()==nickname.lower():
            getid=user[2]
            gethavemoney=int(user[3])
            level=user[4]
            if mode==None:
                lines[index]=lines[index].replace(f"{getid},{'%010d'%gethavemoney}",f"{getid},{'%010d'%(gethavemoney+int(moa))}")
            elif mode==1:
                lines[index]=lines[index].replace(f"{getid},{'%010d'%gethavemoney},{level}",f"{getid},{'%010d'%(gethavemoney+int(moa))},0")
            elif mode==2:
                lines[index]=lines[index].replace(f"{getid},{'%010d'%gethavemoney},{level}",f"{getid},{'%010d'%(gethavemoney-int(moa))},{getlevel}")
            #모드가 2일때 의문의 물건 구매
        
        writetext+=lines[index]
        index+=1

    if not nickname.lower() in nicknames:
        return 0

    with open(f"user_info{ctx.guild.id}","w") as f:
        f.write(writetext)



async def setluckypang(price,ctx,maxlucky):

    file=open("luckypang","r")
    stack=int(file.read())
    file.close()

    
    await ctx.send(f"{stack+price}/{maxlucky}  {'%.3f'%((stack+price)/maxlucky*100)}%")

    if stack+price>=maxlucky:
        nicknames=[]

        userfile=open(f"user_info{ctx.guild.id}","r")
        userlines=userfile.readlines()
        userfile.close()
        for user in userlines:
            userinfo=user.split(',')
            nicknames.append(userinfo[1])
        
    
        nickname=random.choice(nicknames)

        givemoney(ctx,nickname,stack+price)

        file=open("luckypang","w")
        file.write("0")
        file.close()

        await ctx.send(f"{nickname} 럭키팡 당첨! {stack+price}모아 지급!")
    else :
        editfile=open(f"luckypang","w")
        editfile.write(str(stack+price))
        editfile.close()


def GetBeggingMoa():
    i=1
    cut=0
    getmoa=0
    result=random.random()*100
    while i<=12:
        cut+=i
        if result<cut:
            getmoa=32000-1000*(i-1)
            break
        else :
            i+=1
    if i==1:
        result=random.random()*100
        if result<10:
            getmoa*=2
    if i==13 :
        getmoa=2500

    return getmoa