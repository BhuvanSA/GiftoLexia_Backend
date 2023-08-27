import json


f = open("file.json")

data = json.load(f)

for i in data["emp_details"]:
    print(i)

f.close()
