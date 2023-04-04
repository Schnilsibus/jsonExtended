import sys
from pathlib import Path
from json import dumps
sys.path.append("D:\Desktop\jsonExtended")
from _core.jsonx import _indentLevel
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
    "thisaObj": {
        "first": 123,
        "second": None,
        "third": "nowIamBored"
    }
}
invalidJSONData = Path.cwd()

validJSONStr = dumps(validJSONData)
invalidJSONStr = validJSONStr[1:]
indentedValidJSONStr = dumps(validJSONData, indent = _indentLevel)

pathToValidJSON = Path.cwd() / Path(r"tests\validJSONfile.json")
pathToInvalidJSON = Path.cwd() / Path(r"tests\invlaidJSONfile.json")
pathToNoJSON = Path.cwd() / Path(r"tests\idontexist.json")