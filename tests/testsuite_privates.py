import sys
from unittest import main, TestCase
from parameterized import parameterized
from consts import *
sys.path.append("D:\Desktop\jsonExtended")
from _core.json_extended import _contains_key, _get_value_of_keys, _is_json_object, _is_json_property, JSONKeyNotFoundError

class TestSuite__isJSONProperty(TestCase):

    @parameterized.expand(mappedPythonTypes)
    def test_trueForMappedPythonTypes(self, obj: any):
        self.assertTrue(expr = _is_json_property(raw_data= obj), msg =f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_trueForList(self):
        obj = nonEmptyList
        self.assertTrue(expr = _is_json_property(raw_data= obj), msg =f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_trueForEmptyList(self):
        obj = emptyList
        self.assertTrue(expr = _is_json_property(raw_data= obj), msg =f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_falseForDict(self):
        obj = nonEmptyDict
        self.assertFalse(expr = _is_json_property(raw_data= obj), msg =f"the python object '{obj}' is no JSON property, but _isJSONProperty says otherwise")

    def test_falseForEmptyDict(self):
        obj = emptyDict
        self.assertFalse(expr = _is_json_property(raw_data= obj), msg =f"the python object '{obj}' is no JSON property, but _isJSONProperty says otherwise")

class TestSuite__isJSONObject(TestCase):
    
    @parameterized.expand(mappedPythonTypes)
    def test_falseForMappedPythonTypes(self, obj: any):
        self.assertFalse(expr = _is_json_object(raw_data= obj), msg =f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_falseForList(self):
        obj = nonEmptyList
        self.assertFalse(expr = _is_json_object(raw_data= obj), msg =f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_falseForEmptyList(self):
        obj = emptyList
        self.assertFalse(expr = _is_json_object(raw_data= obj), msg =f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_trueForDict(self):
        obj = nonEmptyDict
        self.assertTrue(expr = _is_json_object(raw_data= obj), msg =f"the python object '{obj}' is a JSON object, but _isJSONObject says otherwise")

    def test_trueForEmptyDict(self):
        obj = emptyDict
        self.assertTrue(expr = _is_json_object(raw_data= obj), msg =f"the python object '{obj}' is a JSON object, but _isJSONObject says otherwise")

class TestSuite__containsKey(TestCase):

    def test_trueForKeyInDict(self):
        key = list(nonEmptyDict.keys())[0]
        self.assertTrue(expr = _contains_key(raw_data= nonEmptyDict, key = key), msg =f"The dict '{nonEmptyDict}' contains key '{key}', but _containsKey says otherwise")
    
    def test_falseForEmptyDict(self):
        key = "somekey"
        self.assertFalse(expr = _contains_key(raw_data= emptyDict, key = key), msg =f"The dict '{nonEmptyDict}' is empty, but _containsKey says it contains key '{key}'")

class TestSuite__getValueOfKeys(TestCase):

    def test_returnsObjectForEmptyKeysList(self):
        self.assertTrue(expr =validJSONData == _get_value_of_keys(raw_data= validJSONData, keys = ()), msg ="_getValueOfKeys should return whole obj for empty keys set")

    @parameterized.expand(simpleTypeKeys)
    def test_findsAndReturnsSimpleType(self, key: str):
        self.assertTrue(expr =validJSONData[key] == _get_value_of_keys(raw_data= validJSONData, keys = (key,)), msg =f"_getValueOfKeys does not return key '{key}' correctly")

    def test_findsAndReturnsList(self):
        self.assertTrue(expr =validJSONData[arrayKey] == _get_value_of_keys(raw_data= validJSONData, keys = (arrayKey,)), msg =f"_getValueOfKeys does not return key '{arrayKey}' correctly")

    def test_findsAndReturnsDict(self):
        self.assertTrue(expr =validJSONData[objectKey] == _get_value_of_keys(raw_data= validJSONData, keys = (objectKey,)), msg =f"_getValueOfKeys does not return key '{objectKey}' correctly")

    def test_findsAndReturnsNonTopLevelMember(self):
        self.assertTrue(expr =nonTopLevelValue == _get_value_of_keys(raw_data= validJSONData, keys = nonTopLevelKeys), msg =f"_getValueOfKeys does not return keys '{nonTopLevelKeys}' correctly")

    def tets_raisesErrorIfAKeyDoesNotExist(self):
        try:
            _get_value_of_keys(raw_data= validJSONData, keys = invalidKeys)
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")

if (__name__ == "__main__"):
    main()