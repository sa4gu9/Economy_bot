import json
def seasoncheck(): 
    season=None
    with open("seasoninfo.json","r") as seasonfile:
        season=json.load(seasonfile)
    return season