import json

with open("incidents.json","r") as fd:
    data = json.load(fd)

data_map = {}

for ticket in data["tickets"]:
    p = (ticket["file_hash"], ticket["dst_ip"])
    if(p not in data_map):
        data_map[p] = 1
    else:
        data_map[p] += 1
for key in data_map:
    print(key, data_map[key])

# 2 1 1 2 1
