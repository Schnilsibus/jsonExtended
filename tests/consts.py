import pathlib

initalJSONData = {
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

path = pathlib.Path.cwd() / pathlib.Path(r"test\testJSONfile.json")