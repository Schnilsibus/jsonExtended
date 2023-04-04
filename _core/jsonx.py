import json
import pathlib
from errors import *

_indentLevel = 4

def getProperty(filePath: pathlib.Path, keys: list) -> any:
    rawData = _readJSONFile(filePath = filePath)
    property = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isObject(rawData = property)):
        raise NotAPropertyError(noPropertyObject = property)
    return property

def setProperty(filePath: pathlib.Path, keys: list, value: any):
    rawData = _readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyError(wrongKey = keys[-1], currentKeyList = list(parentObject.keys()), foundKeys = keys[:-1])
    elif (_isObject(rawData = parentObject[keys[-1]])):
        raise NotAPropertyError(noPropertyObject = parentObject[keys[-1]])
    parentObject[keys[-1]] = value
    _writeJSONFile(filePath = filePath, data = rawData)

def addProperty(filePath: pathlib.Path, keys: list, newKey: str, value: any):
    rawData = _readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = list(parentObject.keys()), foundKeys = keys)
    parentObject[newKey] = value
    _writeJSONFile(filePath = filePath, data = rawData)

def getObject(filePath: pathlib.Path, keys: list) -> dict:
    rawData = _readJSONFile(filePath = filePath)
    object = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isProperty(rawData = object)):
        raise NotAObjectError(noObject = object)
    return object

def setObject(filePath: pathlib.Path, keys: list, object: dict):
    rawData = _readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyError(wrongKey = keys[-1], allKeysOfObject = list(parentObject.keys()), foundKeys = keys[:-1])
    elif(_isProperty(rawData = parentObject[keys[-1]])):
        raise NotAObjectError(noObject = parentObject[keys[-1]])
    parentObject[keys[-1]] = object
    _writeJSONFile(filePath = filePath, data = rawData)

def addObject(filePath: pathlib.Path, keys: list, newKey: str, object: dict):
    rawData = _readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = list(parentObject.keys()), foundKeys = keys)
    parentObject[newKey] = object
    _writeJSONFile(filePath = filePath, data = rawData)

def isFormatCorrect(filePath: pathlib.Path) -> bool:
    with open(file = filePath, mode = "r") as fp:
        try:
            json.load(fp = fp)
        except json.JSONDecodeError:
            return False
        return True
    
def indentFile(filePath: pathlib.Path):
    _writeJSONFile(filePath = filePath, data = _readJSONFile(filePath = filePath))

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

def _readJSONFile(filePath: pathlib.Path) -> dict:
    with filePath.open(mode = "r") as fp:
        return json.load(fp = fp)
    
def _writeJSONFile(filePath: pathlib.Path, data: any):
    with filePath.open(mode = "w") as fp:
        json.dump(obj = data, fp = fp, indent = _indentLevel)
