from json import dump, load, JSONDecodeError
from pathlib import Path

_indentLevel = 4

class NotAPropertyError(Exception):
    """
    An Error that is be raised if a python object has a type that is not mapped to a JSON type

    Can also be raised if contents of a JSON file should be a JSON property but are a JSON object.
    JSON types that are called properties are: array, string, number, boolean, null.
    The python types that are mapped to those are: tuple, str, int, float, bool, None.
    Every other python type is not considerd a JSON property.
    """

    def __init__(self, noPropertyObject: any):
        """
        Parameters
        ----------
        noPropertyObject: any
            the python object whose type is not mapped to a JSON property
        """

        Exception.__init__(self, f"the json object {noPropertyObject} is not a property; properties are: json data types and json arrays")

class NotAObjectError(Exception):
    """
    An Error that is be raised if a python object has a type that is not mapped to a JSON object

    Can also be raised if contents of a JSON file should be a JSON object but are a JSON property.
    JSON objects are the objects enclosed in curly braces in json files.
    The python type that is mapped to this is: dict.
    Every other python type is not considerd a JSON object.
    """

    def __init__(self, noObject: any):
        """
        Parameters
        ----------
        noObject: any
            the python object whose type is not mapped to a JSON object
        """

        Exception.__init__(self, f"the json value {noObject} is not a json object")

class JSONKeyNotFoundError(Exception):
    """
    An Error that is be raised if a key is not found in a JSON file
    """

    def __init__(self, wrongKey: str, allKeysOfObject: tuple, foundKeys: tuple = None):
        """
        Parameters
        ----------
        wrongKey: str
            the key that could not be found
        allKeysOfObject: tuple
            all the keys of the object in which the wrong key could not be found
        foundKeys: tuple (default=None)
            all the keys of the parent JSON objects of the object in which the wrong key could not be found
        """
        
        Exception.__init__(self, f"key '{wrongKey}' not in {allKeysOfObject}; found keys: [{'->'.join(foundKeys)}]")

class JSONKeyAlreadyExists(Exception):
    """
    An Error that is be raised if a key already exists in a JSON object
    """
    
    def __init__(self, doubleKey: str, allKeysOfObject: tuple, foundKeys: tuple = None):
        """
        Parameters
        ----------
        doubleKey: str
            the key that already exists
        allKeysOfObject: tuple
            all the keys of the object that already contains the doubled key
        foundKeys: tuple
            all the keys of the parent JSON objects of the object that contains the doubled key
        """
        
        Exception.__init__(self, f"key '{doubleKey}' already exists in {allKeysOfObject}; found keys: [{'->'.join(foundKeys)}]")

def getProperty(filePath: Path, keys: tuple) -> any:
    """
    Returns a property in a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired property; the key of the property is the last element of the tuple

    Returns
    -------
    the specified property

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAPropertyError
        if keys point to a JSON object (not a JSON property)
    """
    
    rawData = readJSONFile(filePath = filePath)
    property = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isJSONObject(rawData = property)):
        raise NotAPropertyError(noPropertyObject = property)
    return property

def setProperty(filePath: Path, keys: tuple, value: any) -> None:
    """
    Sets a property in a JSON file to a value

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired property; the key of the property is the last element of the tuple
    value: any (must be a python type that is mapped to JSON property)
        the new value of the property

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAPropertyError
        - if keys point to a JSON object (not a JSON property)
        - if type(value) is not mapped to a JSON property
    """
    
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyNotFoundError(wrongKey = keys[-1], allKeysOfObject = tuple(parentObject.keys()), foundKeys = keys[:-1])
    elif (_isJSONObject(rawData = parentObject[keys[-1]])):
        raise NotAPropertyError(noPropertyObject = parentObject[keys[-1]])
    elif (not _isJSONProperty(rawData = value)):
        raise NotAPropertyError(noPropertyObject = value)
    parentObject[keys[-1]] = value
    writeJSONFile(filePath = filePath, data = rawData)

def addProperty(filePath: Path, keys: tuple, newKey: str, value: any) -> None:
    """
    adds a JSON property to a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file point to the JSON object that should contain the new property
    newKey: str
        the new key of the property
    value: any (must be a python type that is mapped to JSON property)
        the value of the new property

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAObjectError
        if keys points to a JSON property instead of a JSON object (can't add a proeprty to a property) 
    NotAPropertyError
        if the type(value) is not mapped to a JSON property
    """
    
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (not _isJSONObject(rawData = parentObject)):
        raise NotAObjectError(noObject = parentObject)
    elif (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = tuple(parentObject.keys()), foundKeys = keys)
    elif (not _isJSONProperty(rawData = value)):
        raise NotAPropertyError(noPropertyObject = value, )
    parentObject[newKey] = value
    writeJSONFile(filePath = filePath, data = rawData)

def containsProperty(filePath: Path, keys: tuple) -> bool:
    """
    Returns if a JSON file contains a specified porperty

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired property; the key of the property is the last element of the tuple
    
    Returns
    -------
    - True if the JSON file contains the specified property
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    """
    
    rawData = readJSONFile(filePath = filePath)
    try:
        value = _getValueOfKeys(rawData = rawData, keys = keys)
        return _isJSONProperty(rawData = value)
    except JSONKeyNotFoundError as ex:
        return False

def getObject(filePath: Path, keys: tuple) -> dict:
    """
    Returns a object in a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired object; the key of the object is the last element of the tuple

    Returns
    -------
    the specified object

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAObjectError
        if keys point to a JSON property (not a JSON object)
    """
    
    rawData = readJSONFile(filePath = filePath)
    object = _getValueOfKeys(rawData = rawData, keys = keys)
    if (_isJSONProperty(rawData = object)):
        raise NotAObjectError(noObject = object)
    return object

def setObject(filePath: Path, keys: tuple, object: dict) -> None:
    """
    Sets a object in a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired object; the key of the object is the last element of the tuple
    object: dict
        the new value of the object

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAObjectError
        - if keys point to a JSON property (not a JSON object)
        - if not type(value) == dict 
    """
    
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys[:-1])
    if (not _containsKey(object = parentObject, key = keys[-1])):
        raise JSONKeyNotFoundError(wrongKey = keys[-1], allKeysOfObject = tuple(parentObject.keys()), foundKeys = keys[:-1])
    elif (_isJSONProperty(rawData = parentObject[keys[-1]])):
        raise NotAObjectError(noObject = parentObject[keys[-1]])
    elif (not _isJSONObject(rawData = object)):
        raise NotAObjectError(noObject = object)
    parentObject[keys[-1]] = object
    writeJSONFile(filePath = filePath, data = rawData)

def addObject(filePath: Path, keys: tuple, newKey: str, object: dict) -> None:
    """
    adds a JSON object to a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file point to the JSON object that should contain the new object
    newKey: str
        the new key of the object
    value: dict
        the value of the new object

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the JSON object that the keys before the not-found-key point to)
    NotAObjectError
        - if keys points to a JSONproperty instead of a JSON object (can't add a object to a property) 
        - if the type(value) is not mapped to a JSON object
    """
    
    rawData = readJSONFile(filePath = filePath)
    parentObject = _getValueOfKeys(rawData = rawData, keys = keys)
    if (not _isJSONObject(rawData = parentObject)):
        raise NotAObjectError(noObject = parentObject)
    elif (_containsKey(object = parentObject, key = newKey)):
        raise JSONKeyAlreadyExists(doubleKey = newKey, allKeysOfObject = tuple(parentObject.keys()), foundKeys = keys)
    elif(not _isJSONObject(rawData = object)):
        raise NotAObjectError(noObject = object)
    parentObject[newKey] = object
    writeJSONFile(filePath = filePath, data = rawData)

def containsObject(filePath: Path, keys: tuple) -> bool:
    """
    Returns if a JSON file contains a specified object

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    keys: tuple
        the orderd! keys in the JSON file that contain the desired object; the key of the object is the last element of the tuple
    
    Returns
    -------
    - True if the JSON file contains the specified object
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    """
    
    rawData = readJSONFile(filePath = filePath)
    try:
        value = _getValueOfKeys(rawData = rawData, keys = keys)
        return _isJSONObject(rawData = value)
    except JSONKeyNotFoundError as ex:
        return False

def isFormatCorrect(filePath: Path) -> bool:
    """
    Returns if a file contains valid JSON

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the file

    Returns
    -------
    - True if the file contains valid JSON (== json.laod() doesn't throw a json.JSONDecodeError)
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    """
    
    with open(file = filePath, mode = "r") as fp:
        try:
            readJSONFile(filePath = filePath)
        except JSONDecodeError:
            return False
        return True
    
def indentJSONFile(filePath: Path) -> None:
    f"""
    Indents a JSON file

    The file is indented using the json.dump() method with indent = {_indentLevel}
    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON
    """
    
    writeJSONFile(filePath = filePath, data = readJSONFile(filePath = filePath))

def readJSONFile(filePath: Path) -> dict:
    """
    Reads the contents of a JSON file and returns them as a dict

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file

    Returns
    -------
    The deserialized contents of a JSON file as a dict

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo dosn't contain valid JSON 
    """
    
    if (not filePath.exists()):
        raise FileNotFoundError(f"the JSON file {filePath} doesn't exist")
    with filePath.open(mode = "r") as fp:
        return load(fp = fp)
    
def writeJSONFile(filePath: Path, data: dict) -> None:
    """
    Writes a dict to a JSON file

    Parameters
    ----------
    filePath: pathlib.Path
        the path to the json file
    data: dict
        the data that should be written to the JSON file
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    NotAObjectError
        if not type(data) == dict 
    """
    
    if (not filePath.exists()):
        raise FileNotFoundError(f"the JSON file {filePath} doesn't exist")
    elif (not _isJSONObject(rawData = data)):
        raise NotAObjectError(noObject = data)
    with filePath.open(mode = "w") as fp:
        dump(obj = data, fp = fp, indent = _indentLevel)

def _getValueOfKeys(rawData: dict, keys: tuple) -> any:
    currentObject = rawData
    for i in range(len(keys)):
        if (not _containsKey(object = currentObject, key = keys[i])):
            raise JSONKeyNotFoundError(wrongKey = keys[i], allKeysOfObject = tuple(rawData.keys()), foundKeys = keys[:i])
        currentObject = currentObject[keys[i]]
    return currentObject

def _isJSONProperty(rawData: any) -> bool:
    return type(rawData) in [type(None), float, int, list, bool, str]

def _isJSONObject(rawData: any) -> bool:
    return type(rawData) == dict

def _containsKey(object: dict, key: str) -> bool:
    return key in object.keys()