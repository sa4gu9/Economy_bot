import asyncio
import random
import discord
import datamanage
import os

path = "data/"


def givemoney(ctx, nickname, moa, mode=None, getlevel=None):
    userinfo = datamanage.GetUserData(ctx)

    moa = int(moa)

    if mode == None:
        userinfo["money"] += moa
    elif mode == 1:
        userinfo["money"] += moa
        userinfo["unknownLevel"] = 0
    elif mode == 2:
        userinfo["money"] -= moa
        userinfo["unknownLevel"] = int(getlevel)
    elif mode == 3:
        if userinfo["money"] >= moa:
            userinfo["money"] -= moa
        else:
            return -1

    datamanage.WriteData(ctx, userinfo)


async def setluckypang(price, ctx, maxlucky, datapath):
    filename = f"{datapath}{ctx.guild.id}/luckypang.txt"

    if not os.path.isfile(filename):
        f = open(filename, "w")
        f.write("0")
        f.close()

    f = open(filename, "r")
    stack = int(f.read())
    f.close()

    f = open(filename, "w")
    f.write(str(stack + price))
    f.close()

    await ctx.send(f"{stack+price}/{maxlucky}  {'%.3f'%((stack+price)/maxlucky*100)}%")

    if stack + price >= maxlucky:
        await ctx.send("현재 데이터 구조 변경 작업중이기 때문에 럭키팡을 할 수 없습니다.")
        return

        user = {}

        userfile = open(f"{path}user_info{ctx.guild.id}", "r")
        userlines = userfile.readlines()
        userfile.close()
        for userline in userlines:
            userinfo = userline.split(",")
            user[userinfo[1]] = int(userinfo[3])

        sumMoney = GetSumMoney(ctx)
        while True:
            usernicks = list(user.keys())
            nickname = random.choice(usernicks)
            if user[nickname] / sumMoney[0] * 100 < 10 and len(usernicks) >= 8:
                break
            elif user[nickname] / sumMoney[0] * 100 < 20 and len(usernicks) >= 6:
                break
            elif user[nickname] / sumMoney[0] * 100 < 30 and len(usernicks) >= 4:
                break
            elif user[nickname] / sumMoney[0] * 100 < 55 or len(usernicks) == 1:
                break

        givemoney(ctx, nickname, stack + price)

        file = open(f"{path}luckypang", "w")
        file.write("0")
        file.close()

        await ctx.send(f"{nickname} 럭키팡 당첨! {stack+price}모아 지급!")
    else:
        editfile = open(f"{path}luckypang", "w")
        editfile.write(str(stack + price))
        editfile.close()


async def GetLuckypang(ctx, maxlucky):
    file = open(f"{path}luckypang", "r")
    stack = int(file.read())
    file.close()

    await ctx.send(f"{stack}/{maxlucky}  {'%.3f'%(stack/maxlucky*100)}%")


def GetBeggingMoa():
    i = 1
    cut = 0
    getmoa = 0
    result = random.random() * 100
    while i <= 12:
        cut += i
        if result < cut:
            getmoa = 32000 - 1000 * (i - 1)
            break
        else:
            i += 1
    if i == 1:
        result = random.random() * 100
        if result < 10:
            getmoa *= 2
    if i == 13:
        getmoa = 2500

    return getmoa


def GetSumMoney(ctx):
    sum_money = 0
    countUser = 0

    directory = f"{path}{ctx.guild.id}"

    file_list = os.listdir(directory)

    file = open(f"{path}{ctx.guild.id}/user_info{ctx.guild.id}", "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        user = line.split(",")
        sum_money += int(user[3])
        countUser += 1

    return sum_money, countUser
