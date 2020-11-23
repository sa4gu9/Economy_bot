import os
import glob
import shutil

def datareset(ctx):

    shutil.rmtree("data/")
    shutil.copytree("default/","data/")


    #거래시장 매물 삭제
    if os.path.isfile("trade.csv"):
        os.remove(f"trade.csv")

    #복권보유정보 삭제
    if os.path.isfile(f"lotto_{ctx.id}"):
        os.remove(f"lotto_{ctx.id}")
    

    return