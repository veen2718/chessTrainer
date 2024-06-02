import json

with open('eco.json', 'r+') as ecojson:
    x1 = json.load(ecojson)
    json.dump(x1,ecojson,indent=2)