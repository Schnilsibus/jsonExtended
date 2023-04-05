import sys
from unittest import main, TestCase
from parameterized import parameterized
from consts import *
sys.path.append("D:\Desktop\jsonExtended")
from _core.jsonx import _containsKey, _getValueOfKeys, _isJSONObject, _isJSONProperty

class TestSuite__isJSONProperty(TestCase):

    @parameterized.expand(jsonProperties)
    def test_trueForJSONProperties(self, obj: any):
        self.assertTrue(expr = _isJSONProperty(rawData = obj), msg = f"the obj {obj} is a JSON property, but _isJSONProperty say otherwise")