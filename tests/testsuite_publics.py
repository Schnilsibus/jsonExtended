import sys
from unittest import main, TestCase
from parameterized import parameterized
from consts import *
from json import load
sys.path.append("D:\Desktop\jsonExtended")
from _core.jsonx import *

class SuperTestClass(TestCase):

    def setUp(self):
        globalSetUp(write = True)

    def tearDown(self):
        globalTearDown()

class TestSuite_isFormatCorrect(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            isFormatCorrect(filePath = pathToNoJSON)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_trueForValidJSONFile(self):
        self.assertTrue(expr = isFormatCorrect(filePath = pathToValidJSON), msg = "isFormatCorrect says format is not correct even though it is")

    def test_falseForInvalidJSONFile(self):
        self.assertFalse(expr = isFormatCorrect(filePath = pathToInvalidJSON), msg = "isFormatCorrect says format is correct even though it is not")

class TestSuite_indentJSONFile(SuperTestClass):
    
    def test_raisesErrorIfPathInvalid(self):
        try:
            indentJSONFile(filePath = pathToNoJSON)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_indentsFileCorrectly(self):
        indentJSONFile(filePath = pathToValidJSON)
        with open(file = pathToValidJSON, mode = "r") as fp:
            fileStr = fp.read()
        self.assertTrue(expr = fileStr == indentedValidJSONStr, msg = "the file is not correctly indented")

class TestSuite_getProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            getProperty(filePath = pathToNoJSON, keys = ())
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            getProperty(filePath = pathToInvalidJSON, keys = ())
            self.fail(msg = "this should have raised a JSONDecodeError")
        except JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            getProperty(filePath = pathToValidJSON, keys = (objectKey,))
            self.fail(msg = "this should have raised a NotAPropertyError")
        except NotAPropertyError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a NotAPropertyError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            getProperty(filePath = pathToValidJSON, keys = invalidKeys)
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")

    @parameterized.expand(simpleTypeKeys)
    def test_returnsSimpleJSONPropertiesCorrectly(self, key: str):
        self.assertTrue(expr = validJSONData[key] == getProperty(filePath = pathToValidJSON, keys = (key,)), msg = "getProperty return wrong value")

    def test_returnsJSONArrayCorrectly(self):
        self.assertTrue(expr = validJSONData[arrayKey] == getProperty(filePath = pathToValidJSON, keys = (arrayKey,)), msg = "getProperty return wrong value")

class TestSuite_setProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            setProperty(filePath = pathToNoJSON, keys = (), value = None)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            setProperty(filePath = pathToInvalidJSON, keys = (), value = None)
            self.fail(msg = "this should have raised a JSONDecodeError")
        except JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            setProperty(filePath = pathToValidJSON, keys = (objectKey,), value = None)
            self.fail(msg = "this should have raised a NotAPropertyError")
        except NotAPropertyError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a NotAPropertyError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            setProperty(filePath = pathToValidJSON, keys = invalidKeys, value = None)
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")
    
    @parameterized.expand(list(simpleTypeKeysWithNewValues.keys()))
    def test_writesSimpleJSONPropertiesCorrectly(self, key: str):
        setProperty(filePath = pathToValidJSON, keys = (key,), value = simpleTypeKeysWithNewValues[key])
        with open(file = pathToValidJSON, mode = "r") as fp:
            self.assertTrue(expr = simpleTypeKeysWithNewValues[key] == load(fp = fp)[key], msg = "after calling setProperty value is not written correctly to the file")
        
    def test_writesJSONArrayCorrectly(self):
        setProperty(filePath = pathToValidJSON, keys = (arrayKey,), value = newArray)
        with open(file = pathToValidJSON, mode = "r") as fp:
            self.assertTrue(expr = newArray == load(fp = fp)[arrayKey], msg = "after calling setProperty value is not written correctly to the file")

class TestSuite_addProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            addProperty(filePath = pathToNoJSON, keys = (), newKey = "", value = None)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            addProperty(filePath = pathToInvalidJSON, keys = (), newKey = "", value = None)
            self.fail(msg = "this should have raised a JSONDecodeError")
        except JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            addProperty(filePath = pathToValidJSON, keys = (), newKey = "", value = invalidJSONData)
            self.fail(msg = "this should have raised a TypeError")
        except TypeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a TypeError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            addProperty(filePath = pathToValidJSON, keys = invalidKeys, newKey = "", value = None)
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONKeyNotFoundError")

    def test_raisesErrorIfNewKeyAlreadyExists(self):
        try:
            addProperty(filePath = pathToValidJSON, keys = (), newKey = arrayKey, value = None)
            self.fail(msg = "this should have raised a JSONKeyAlreadyExists")
        except JSONKeyAlreadyExists as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONKeyAlreadyExists")

    @parameterized.expand(mappedPythonTypes)
    def test_writesSimpleJSONPropertiesCorrectly(self, newVal: str):
        newKey = "newKey"
        addProperty(filePath = pathToValidJSON, keys = (), newKey = newKey, value = newVal)
        with open(file = pathToValidJSON, mode = "r") as fp:
            self.assertTrue(expr = newVal == load(fp = fp)[newKey], msg = "after calling addProperty the property is not written correctly in the json file")

    def test_writesArrayCorrectly(self):
        newKey = "newKey"
        addProperty(filePath = pathToValidJSON, keys = (), newKey = newKey, value = newArray)
        with open(file = pathToValidJSON, mode = "r") as fp:
            self.assertTrue(expr = newArray == load(fp = fp)[newKey], msg = "after calling addProperty the property is not written correctly in the json file")

class TestSuite_containsProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            containsProperty(filePath = pathToNoJSON, keys = ())
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            containsProperty(filePath = pathToInvalidJSON, keys = ())
            self.fail(msg = "this should have raised a JSONDecodeError")
        except JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONDecodeError")

    def test_falseIfKeysEmpty(self):
        self.assertFalse(expr = containsProperty(filePath = pathToValidJSON, keys = ()), msg = "containsProperty returned True for a emptyy key set")

    def test_falseIfPropertyDoesntExist(self):
        self.assertFalse(expr = containsProperty(filePath = pathToValidJSON, keys = invalidKeys), msg = "containsProperty returned True for a property that doesn't exist")

    def test_falseIfKeysPointToObject(self):
        self.assertFalse(expr = containsProperty(filePath = pathToValidJSON, keys = (objectKey,)), msg = "key set points to json object, but containsProeprty returned True")

    @parameterized.expand(simpleTypeKeys)
    def test_trueIfPropertyExists(self, key: str):
        self.assertTrue(expr = containsProperty(filePath = pathToValidJSON, keys = (key,)), msg = f"containsPropety says that property '{(key,)}' doesn't exist but it does")

class TestSuite_getObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            getObject(filePath = pathToNoJSON, keys = ())
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

class TestSuite_setObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            setObject(filePath = pathToNoJSON, keys = (), object = None)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

class TestSuite_addObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            addObject(filePath = pathToNoJSON, keys = (), newKey = "", object = None)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

class TestSuite_containsObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            containsObject(filePath = pathToNoJSON, keys = ())
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

if (__name__ == "__main__"):
    main()