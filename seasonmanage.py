import json
def seasoncheck(): 
    season=None
    with open("data/seasoninfo.json","r") as seasonfile:
        season=json.load(seasonfile)
    return season