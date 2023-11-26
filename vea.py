import json
a = {
    "miguel":"tom",
    "ana":"hk",
    "pepe":"hello"
    }
with open('logins.json',mode='w') as archivo:
    json.dump(a , archivo , indent=4)
