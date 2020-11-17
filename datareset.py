import os
import glob
import shutil

def datareset(ctx):
    #럭키팡, 강화매물 0으로 리셋
    os.remove("luckypang")
    shutil.copy("../default/luckypang","./")
    os.remove("forcestore")
    shutil.copy("../default/forcestore","./")

    #유저 정보 삭제
    os.remove(f"user_info{ctx.id}")

    #거래시장 매물 삭제
    if os.path.isfile("trade.csv"):
        os.remove(f"trade.csv")

    #복권보유정보 삭제
    if os.path.isfile(f"lotto_{ctx.id}"):
        os.remove(f"lotto_{ctx.id}")
    

    #아이템보유정보 삭제
    fileList = glob.glob('./forceitem*')
    print(fileList)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

    #프리시즌 전환
    prefile=open("ispreseason","w")
    prefile.write("true,preseason")
    prefile.close()
    return