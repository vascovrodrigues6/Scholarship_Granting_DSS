import json

def readJson(file_name):
    f = open(file_name + '.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

def writeJson(file_name, lines):
    with open(file_name + '.json', 'w') as outfile:
        json.dump(lines, outfile, indent = 2)