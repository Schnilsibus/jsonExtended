import json

_indentLevel = 4


class NotAPropertyError(Exception):
    def __init__(self, noPropertyObject: dict):
        Exception.__init__(self, f"the json object {noPropertyObject} is not a property; properties are: json data types and json arrays")

class JSONKeyError(Exception):
    def __init__(self, wrongKey: str, currentKeyList: list, foundKeys: list = None):
        Exception.__init__(self, f"key '{wrongKey}' not in {currentKeyList}; found keys: [{'->'.join(foundKeys)}]")

class JSONKeyAlreadyExists(Exception):
    def __init__(self, doubleKey: str, currentKeyList: list, foundKeys: list = None):
        Exception.__init__(self, f"key '{doubleKey}' already exists in {currentKeyList}; found keys: [{{'->'.join(foundKeys)}}]")

def _getValueOfKeys(rawData: dict, keys: list) -> any:
    currentObject = rawData
    for i in range(len(keys)):
        if (not _containsKey(object = currentObject, key = keys[i])):
            raise JSONKeyError(wrongKey = keys[i], currentKeyList = list(rawData.keys()), foundKeys = keys[:i])
        currentObject = currentObject[keys[i]]
    return currentObject

def _isProperty(rawData: any) -> bool:
    return not _isObject(rawData = rawData)

def _isObject(rawData: any) -> bool:
    return type(rawData) == dict

def _containsKey(object: dict, key: str) -> bool:
    return key in object.keys()

def loadProperty(filePath: str, keys: list) -> any:
    rawData = readJSONFile(filePath = filePath)
    property = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isObject(rawData = property)):
        raise NotAPropertyError(noPropertyObject = property)
    return property

def setProperty(filePath: str, keys: list, value: any):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        return JSONKeyError(wrongKey = keys[-1], currentKeyList = list(parentObject.keys()), foundKeys = keys[:-1])
    elif (_isObject(rawData = parentObject[keys[-1]])):
        return NotAPropertyError(noPropertyObject = parentObject[keys[-1]])
    parentObject[keys[-1]] = value
    writeJSONFile(filePath = filePath, data = rawData)

def addProperty(filePath: str, keys: list, newKey: str, value: any):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists()
    parentObject[newKey] = value
    writeJSONFile(filePath = filePath, data = rawData)

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
