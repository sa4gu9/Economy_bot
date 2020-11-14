def seasoncheck():
    seasonfile=open("ispreseason","r")
    seasoncheck=seasonfile.read().split(',')
    seasonfile.close()

    return seasoncheck