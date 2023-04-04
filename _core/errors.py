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
