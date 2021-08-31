import os
import glob
import shutil
import json


def datareset(ctx):

    shutil.rmtree("data/")
    shutil.copytree("default/", "data/")

    # 거래시장 매물 삭제
    if os.path.isfile("trade.csv"):
        os.remove(f"trade.csv")

    # 복권보유정보 삭제
    if os.path.isfile(f"lotto_{ctx.id}"):
        os.remove(f"lotto_{ctx.id}")

    return


def WriteData(ctx, data):
    fileName = f"data/{ctx.guild.id}/{ctx.author.id}.json"

    with open(fileName, "w") as f:
        json.dump(data, f)


def GetAllUserData(ctx):
    dirName = f"data/{ctx.guild.id}"
    fileList = os.listdir(dirName)
    userlist = {}

    for fname in fileList:
        if fname[0:4].isdigit():
            with open(dirName + "/" + fname) as f:
                userinfo = json.load(f)
                userlist[fname.replace(".json", "")] = userinfo
    return userlist


def GetUserData(ctx, ids=None):
    userData = None
    if ids == None:
        fileName = f"data/{ctx.guild.id}/{ctx.author.id}.json"
        if os.path.isfile(fileName):
            with open(fileName, "r") as f:
                userData = json.load(f)
    else:
        fileName = f"data/{ctx.guild.id}/{ids}.json"
        if os.path.isfile(fileName):
            with open(fileName, "r") as f:
                userData = json.load(f)
    return userData


def GetFileName(ctx):
    return f"data/{ctx.guild.id}/{ctx.author.id}.json"
