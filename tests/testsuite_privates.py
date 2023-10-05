from unittest import main, TestCase
from parameterized import parameterized
from consts import *
import _core.json_extended as jsonx


class TestSuiteIsJSONProperty(TestCase):

    @parameterized.expand(mappedPythonTypes)
    def test_trueForMappedPythonTypes(self, obj: any):
        self.assertTrue(expr=jsonx._is_json_property(raw_data=obj),
                        msg=f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_trueForList(self):
        obj = nonEmptyList
        self.assertTrue(expr=jsonx._is_json_property(raw_data=obj),
                        msg=f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_trueForEmptyList(self):
        obj = emptyList
        self.assertTrue(expr=jsonx._is_json_property(raw_data=obj),
                        msg=f"the python object '{obj}' is a JSON property, but _isJSONProperty says otherwise")

    def test_falseForDict(self):
        obj = nonEmptyDict
        self.assertFalse(expr=jsonx._is_json_property(raw_data=obj),
                         msg=f"the python object '{obj}' is no JSON property, but _isJSONProperty says otherwise")

    def test_falseForEmptyDict(self):
        obj = emptyDict
        self.assertFalse(expr=jsonx._is_json_property(raw_data=obj),
                         msg=f"the python object '{obj}' is no JSON property, but _isJSONProperty says otherwise")


class TestSuiteIsJSONObject(TestCase):

    @parameterized.expand(mappedPythonTypes)
    def test_falseForMappedPythonTypes(self, obj: any):
        self.assertFalse(expr=jsonx._is_json_object(raw_data=obj),
                         msg=f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_falseForList(self):
        obj = nonEmptyList
        self.assertFalse(expr=jsonx._is_json_object(raw_data=obj),
                         msg=f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_falseForEmptyList(self):
        obj = emptyList
        self.assertFalse(expr=jsonx._is_json_object(raw_data=obj),
                         msg=f"the python object '{obj}' is no JSON object, but _isJSONObject says otherwise")

    def test_trueForDict(self):
        obj = nonEmptyDict
        self.assertTrue(expr=jsonx._is_json_object(raw_data=obj),
                        msg=f"the python object '{obj}' is a JSON object, but _isJSONObject says otherwise")

    def test_trueForEmptyDict(self):
        obj = emptyDict
        self.assertTrue(expr=jsonx._is_json_object(raw_data=obj),
                        msg=f"the python object '{obj}' is a JSON object, but _isJSONObject says otherwise")


class TestSuiteContainsKey(TestCase):

    def test_trueForKeyInDict(self):
        key = list(nonEmptyDict.keys())[0]
        self.assertTrue(expr=jsonx._contains_key(raw_data=nonEmptyDict, key=key),
                        msg=f"The dict '{nonEmptyDict}' contains key '{key}', but _containsKey says otherwise")

    def test_falseForEmptyDict(self):
        key = "key"
        self.assertFalse(expr=jsonx._contains_key(raw_data=emptyDict, key=key),
                         msg=f"The dict '{nonEmptyDict}' is empty, but _containsKey says it contains key '{key}'")


class TestSuiteGetValueOfKeys(TestCase):

    def test_returnsObjectForEmptyKeysList(self):
        self.assertTrue(expr=validJSONData == jsonx._get_value_of_keys(raw_data=validJSONData, keys=()),
                        msg="_getValueOfKeys should return whole obj for empty keys set")

    @parameterized.expand(simpleTypeKeys)
    def test_findsAndReturnsSimpleType(self, key: str):
        self.assertTrue(expr=validJSONData[key] == jsonx._get_value_of_keys(raw_data=validJSONData, keys=(key,)),
                        msg=f"_getValueOfKeys does not return key '{key}' correctly")

    def test_findsAndReturnsList(self):
        self.assertTrue(
            expr=validJSONData[arrayKey] == jsonx._get_value_of_keys(raw_data=validJSONData, keys=(arrayKey,)),
            msg=f"_getValueOfKeys does not return key '{arrayKey}' correctly")

    def test_findsAndReturnsDict(self):
        self.assertTrue(
            expr=validJSONData[objectKey] == jsonx._get_value_of_keys(raw_data=validJSONData, keys=(objectKey,)),
            msg=f"_getValueOfKeys does not return key '{objectKey}' correctly")

    def test_findsAndReturnsNonTopLevelMember(self):
        self.assertTrue(expr=nonTopLevelValue == jsonx._get_value_of_keys(raw_data=validJSONData, keys=nonTopLevelKeys),
                        msg=f"_getValueOfKeys does not return keys '{nonTopLevelKeys}' correctly")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            jsonx._get_value_of_keys(raw_data=validJSONData, keys=invalidKeys)
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except jsonx.JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")


if __name__ == "__main__":
    main()
