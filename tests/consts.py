import pathlib
import json

validJSONStr = """{
    "thisastr": "IamAString",
    "thisaint": 1234,
    "thisafloat": -56.78,
    "thisabool": true,
    "thisnull": null,
    "thisaarray": [
        "str",
        -23,
        4.5,
        false,
        null
    ],
    "thisaObj": {
        "first": 123,
        "second": null,
        "third": "nowIamBored"
    }
}
"""

invalidJSONStr = """"thisastr": "IamAString",
    "thisaint": 1234,
    "thisafloat": -56.78,
    "thisabool": true,
    "thisnull": null,
    "thisaarray": [
        "str",
        -23,
        4.5,
        false,
        null
    ],
    "thisaObj": {
        "first": 123,
        "second": null,
        "third": "nowIamBored"
    }
}
"""

validJSONData = json.loads(s = validJSONStr)

pathToValidJSON = pathlib.Path.cwd() / pathlib.Path(r"tests\validJSONfile.json")
pathToInvalidJSON = pathlib.Path.cwd() / pathlib.Path(r"tests\invlaidJSONfile.json")
pathToNoJSON = pathlib.Path.cwd() / pathlib.Path(r"tests\idontexist.json")