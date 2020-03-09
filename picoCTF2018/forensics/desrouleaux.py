import json

with open("incidents.json","r") as fd:
    f = json.load(fd)

for i in f:
    print(i)
