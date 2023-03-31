import json
import os

_indentLevel = 4

class JSONKeyError(Exception):
    def __init__(self, wrongKey: str, currentKeyList: list, foundKeys: list):
        Exception.__init__(self, f"key '{wrongKey}' not in {currentKeyList}; found keys: [{'->'.join(foundKeys)}]")

def loadProperty(filePath: str, keys: list) -> any:
    rawData = readJSONFile(filePath = filePath)
    for i in range(len(keys)):
        if (keys[i] not in rawData.keys()):
            raise JSONKeyError(wrongKey = keys[i], currentKeyList = list(rawData.keys()), foundKeys = keys[:i])
        rawData = rawData[keys[i]]
    return rawData

def setProperty(filePath: str, keys: list, value):
    raise NotImplementedError()

def addProperty(filePath: str, keys: list, value):
    raise NotImplementedError()

def isFormatCorrect(filePath: str) -> bool:
    with open(file = filePath, mode = "r") as fp:
        try:
            json.load(fp = fp)
        except json.JSONDecodeError:
            return False
        return True
    
def indentFile(filePath: str):
    writeJSONFile(filePath = filePath, data = readJSONFile(filePath = filePath))

def readJSONFile(filePath: str) -> dict:
    with open(file = filePath, mode = "r") as fp:
        return json.load(fp = fp)
    
def writeJSONFile(filePath: str, data: any):
    with open(file = filePath, mode = "w") as fp:
        json.dump(obj = data, fp = fp, indent = _indentLevel)
