import sys
from pathlib import Path
from json import dumps
sys.path.append("D:\Desktop\jsonExtended")
from _core.json_extended import _indent_level
validJSONData = {
    "thisastr": "IamAString",
    "thisaint": 1234,
    "thisafloat": -56.78,
    "thisabool": True,
    "thisnull": None,
    "thisaarray": [
        "str",
        -23,
        4.5,
        False,
        None
    ],
    "thisaobj": {
        "first": 123,
        "second": None,
        "third": "nowIamBored"
    }
}
invalidJSONData = Path.cwd()

simpleTypeKeys = [
    "thisastr",
    "thisaint",
    "thisafloat",
    "thisabool",
    "thisnull"
]
arrayKey = "thisaarray"
objectKey = "thisaobj"
nonTopLevelKeys = ("thisaobj", "second")
nonTopLevelValue = validJSONData["thisaobj"]["second"]
invalidKeys = ("thisaobj", "thisnothere")

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
indentedValidJSONStr = dumps(validJSONData, indent = _indent_level)

pathToValidJSON = Path.cwd() / Path(r"tests\validJSONfile.json")
pathToInvalidJSON = Path.cwd() / Path(r"tests\invlaidJSONfile.json")
pathToNoJSON = Path.cwd() / Path(r"tests\idontexist.json")

mappedPythonTypes = [
        "astring",
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

nonEmptyDict = {"astr": "str", "aint": -3, "afloat": 10.5, "abool": True, "aNull": None}
emptyDict = {}

def globalSetUp(write: bool):
    open(file = pathToValidJSON, mode = "x").close()
    open(file = pathToInvalidJSON, mode = "x").close()
    if (write):
        with open(file = pathToValidJSON, mode = "w") as fp:
                fp.write(validJSONStr)
        with open(file = pathToInvalidJSON, mode = "w") as fp:
                fp.write(invalidJSONStr)

def globalTearDown():
    pathToValidJSON.unlink()
    pathToInvalidJSON.unlink()
    if (pathToNoJSON.exists()):
        pathToNoJSON.unlink()