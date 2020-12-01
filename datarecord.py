from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime

scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials=ServiceAccountCredentials.from_json_keyfile_name(
    './studious-loader-270209-7a3790381f5e.json',scope
)
gc=gspread.authorize(credentials)

def SetWorkFileSheet(testmode):
    workfile=None
    if testmode :
        workfile=gc.open("모아봇 테스트 서버 통계")
    else :
        workfile=gc.open("모아봇 자산 통계")
    
    return workfile

def createsheet(seasoncheck,testmode):
    workfile=SetWorkFileSheet(testmode)
    sheetName=GetSheetName(seasoncheck)

    sheet=workfile.add_worksheet(sheetName,rows=1,cols=1)
    sheet.update_acell('A1','닉네임')

def GetSheetName(seasoncheck):
    print(seasoncheck)
    if seasoncheck['ispreseason']:
        return f"프리시즌{seasoncheck['currentseason']}-{seasoncheck['resetcount']}"
    else:
        return f"시즌{seasoncheck['currentseason']}"

def AddNickname(seasoncheck,testmode,nickname):
    workfile=SetWorkFileSheet(testmode)
    sheetName=GetSheetName(seasoncheck)

    sheet=workfile.worksheet(sheetName)
    sheet.add_cols(1)
    colcount=sheet.col_count+1
    sheet.update_cell(1,colcount,nickname)

    

def RecordData(ctx,seasoncheck,testmode):
    file=open(f"data/user_info{ctx.guild.id}","r")
    lines=file.readlines()
    file.close()
    userlist={}

    for line in lines :
        user=line.split(',')
        userlist[user[1]]=int(user[3])


    workfile=SetWorkFileSheet(testmode)
    sheetName=GetSheetName(seasoncheck)

    sheet=workfile.worksheet(sheetName)


    nowtime=datetime.datetime.now()
    
    

    year=nowtime.year
    month=nowtime.month
    day=nowtime.day
    hour=nowtime.hour
    minute=nowtime.minute

    timestring=f"{year}-{month}-{day} {hour}:{'%02d'%minute}"
    writelist=[timestring]

    for value in userlist.values():
        writelist.append(value)

    sheet.append_row(writelist)

    

    