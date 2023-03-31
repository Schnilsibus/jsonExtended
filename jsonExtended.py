import json

indentLevel = 4

def loadProperty(filePath: str, propertyPath: list) -> any:
    with open(file = filePath, mode = "r") as fp:
        content = fp.read()
        rawData = json.load(fp = fp)
    for name in propertyPath:
        rawData = rawData[name]
    return rawData

def setProperty(filePath: str, propertyPath: list, value):
    with open(file = filePath, mode = "r") as fp:
        rawData = json.load(fp = fp)
    relevantData = rawData
    for name in propertyPath:
        relevantData = relevantData[name]
    relevantData = value
    with open(file = filePath, mode = "w") as fp:
        json.dump(obj = rawData, fp = fp, indent = indentLevel)


def addProperty(filePath: str, propertyPath: list, value):
    with open(file = filePath, mode = "r") as fp:
        rawData = json.load(fp = fp)
    relevantData = rawData
    for name in propertyPath[:-1]:
        relevantData = relevantData[name]
    relevantData[propertyPath[-1]] = value
    with open(file = filePath, mode = "w") as fp:
        json.dump(obj = rawData, fp = fp, indent = indentLevel)