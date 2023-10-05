from pathlib import Path
from json import dumps

indent_level = 4

validJSONData = {
    "string": "IamAString",
    "integer": 1234,
    "floating-point": -56.78,
    "boolean": True,
    "null": None,
    "list": [
        "str",
        -23,
        4.5,
        False,
        None
    ],
    "object": {
        "first": 123,
        "second": None,
        "third": "nowIamBored"
    }
}
invalidJSONData = Path.cwd()

simpleTypeKeys = [
    "string",
    "integer",
    "floating-point",
    "boolean",
    "null"
]
arrayKey = "list"
objectKey = "object"
nonTopLevelKeys = ("object", "second")
nonTopLevelValue = validJSONData["object"]["second"]
invalidKeys = ("object", "invalid")

newArray = [
    "newString",
    100,
    -45.78,
    False,
    None
]
simpleTypeKeysWithNewValues = {simpleTypeKeys[i]: newArray[i] for i in range(len(simpleTypeKeys))}

validJSONStr = dumps(validJSONData)
invalidJSONStr = validJSONStr[1:]
indentedValidJSONStr = dumps(validJSONData, indent=indent_level)


this_dir = Path(__file__).parent
pathToValidJSON = this_dir / Path("valid_json_file.json")
pathToInvalidJSON = this_dir / Path("invalid_json_file.json")
pathToNoJSON = this_dir / Path("dont_exist.json")

mappedPythonTypes = [
    "string",
    "",
    10,
    -10,
    0,
    -0,
    123.345,
    -3.7,
    0.0,
    -0.0,
    True,
    False,
    None
]

nonEmptyList = ["str", -3, 10.5, True, None]
emptyList = []

nonEmptyDict = {"string": "str", "int": -3, "afloat": 10.5, "bool": True, "none": None}
emptyDict = {}


def globalSetUp(write: bool):
    open(file=pathToValidJSON, mode="x").close()
    open(file=pathToInvalidJSON, mode="x").close()
    if write:
        with open(file=pathToValidJSON, mode="w") as fp:
            fp.write(validJSONStr)
        with open(file=pathToInvalidJSON, mode="w") as fp:
            fp.write(invalidJSONStr)


def globalTearDown():
    pathToValidJSON.unlink()
    pathToInvalidJSON.unlink()
    if pathToNoJSON.exists():
        pathToNoJSON.unlink()
