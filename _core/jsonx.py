from json import dump, load, JSONDecodeError
from pathlib import Path

_indentLevel = 4

class NotAPropertyError(Exception):
    def __init__(self, noPropertyObject: dict):
        Exception.__init__(self, f"the json object {noPropertyObject} is not a property; properties are: json data types and json arrays")

class NotAObjectError(Exception):
    def __init__(self, noObject: any):
        Exception.__init__(self, f"the json value {noObject} is not a json object")

class JSONKeyError(Exception):
    def __init__(self, wrongKey: str, allKeysOfObject: list, foundKeys: list = None):
        Exception.__init__(self, f"key '{wrongKey}' not in {allKeysOfObject}; found keys: [{'->'.join(foundKeys)}]")

class JSONKeyAlreadyExists(Exception):
    def __init__(self, doubleKey: str, allKeysOfObject: list, foundKeys: list = None):
        Exception.__init__(self, f"key '{doubleKey}' already exists in {allKeysOfObject}; found keys: [{{'->'.join(foundKeys)}}]")

def getProperty(filePath: Path, keys: set) -> any:
    rawData = readJSONFile(filePath = filePath)
    property = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isJSONObject(rawData = property)):
        raise NotAPropertyError(noPropertyObject = property)
    return property

def setProperty(filePath: Path, keys: set, value: any):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyError(wrongKey = keys[-1], currentKeyList = set(parentObject.keys()), foundKeys = keys[:-1])
    elif (_isJSONObject(rawData = parentObject[keys[-1]])):
        raise NotAPropertyError(noPropertyObject = parentObject[keys[-1]])
    parentObject[keys[-1]] = value
    writeJSONFile(filePath = filePath, data = rawData)

def addProperty(filePath: Path, keys: set, newKey: str, value: any):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = set(parentObject.keys()), foundKeys = keys)
    parentObject[newKey] = value
    writeJSONFile(filePath = filePath, data = rawData)

def getObject(filePath: Path, keys: set) -> dict:
    rawData = readJSONFile(filePath = filePath)
    object = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isJSONProperty(rawData = object)):
        raise NotAObjectError(noObject = object)
    return object

def setObject(filePath: Path, keys: set, object: dict):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyError(wrongKey = keys[-1], allKeysOfObject = set(parentObject.keys()), foundKeys = keys[:-1])
    elif(_isJSONProperty(rawData = parentObject[keys[-1]])):
        raise NotAObjectError(noObject = parentObject[keys[-1]])
    parentObject[keys[-1]] = object
    writeJSONFile(filePath = filePath, data = rawData)

def addObject(filePath: Path, keys: set, newKey: str, object: dict):
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = set(parentObject.keys()), foundKeys = keys)
    parentObject[newKey] = object
    writeJSONFile(filePath = filePath, data = rawData)

def isFormatCorrect(filePath: Path) -> bool:
    with open(file = filePath, mode = "r") as fp:
        try:
            readJSONFile(filePath = filePath)
        except JSONDecodeError:
            return False
        return True
    
def indentJSONFile(filePath: Path):
    writeJSONFile(filePath = filePath, data = readJSONFile(filePath = filePath))

def readJSONFile(filePath: Path) -> dict:
    if (not filePath.exists()):
        raise FileNotFoundError(f"the JSON file {filePath} doesn't exist")
    with filePath.open(mode = "r") as fp:
        return load(fp = fp)
    
def writeJSONFile(filePath: Path, data: dict):
    if (not filePath.exists()):
        raise FileNotFoundError(f"the JSON file {filePath} doesn't exist")
    with filePath.open(mode = "w") as fp:
        dump(obj = data, fp = fp, indent = _indentLevel)

def _getValueOfKeys(rawData: dict, keys: set) -> any:
    currentObject = rawData
    for i in range(len(keys)):
        if (not _containsKey(object = currentObject, key = keys[i])):
            raise JSONKeyError(wrongKey = keys[i], currentKeyList = set(rawData.keys()), foundKeys = keys[:i])
        currentObject = currentObject[keys[i]]
    return currentObject

def _isJSONProperty(rawData: any) -> bool:
    return type(rawData) in [type(None), float, int, list, bool, str]

def _isJSONObject(rawData: any) -> bool:
    return type(rawData) == dict

def _containsKey(object: dict, key: str) -> bool:
    return key in object.keys()