from unittest import main, TestCase
from parameterized import parameterized
from consts import *
from _core.json_extended import *


class SuperTestClass(TestCase):

    def setUp(self):
        globalSetUp(write=True)

    def tearDown(self):
        globalTearDown()


class TestSuiteIsFormatCorrect(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            is_format_correct(file_path=pathToNoJSON)
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_trueForValidJSONFile(self):
        self.assertTrue(expr=is_format_correct(file_path=pathToValidJSON),
                        msg="isFormatCorrect says format is not correct even though it is")

    def test_falseForInvalidJSONFile(self):
        self.assertFalse(expr=is_format_correct(file_path=pathToInvalidJSON),
                         msg="isFormatCorrect says format is correct even though it is not")


class TestSuiteIndentJSONFile(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            indent_json_file(file_path=pathToNoJSON)
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_indentsFileCorrectly(self):
        indent_json_file(file_path=pathToValidJSON)
        with open(file=pathToValidJSON, mode="r") as fp:
            fileStr = fp.read()
        self.assertTrue(expr=fileStr == indentedValidJSONStr, msg="the file is not correctly indented")


class TestSuiteGetProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            get_property(file_path=pathToNoJSON, keys=())
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            get_property(file_path=pathToInvalidJSON, keys=())
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            get_property(file_path=pathToValidJSON, keys=(objectKey,))
            self.fail(msg="this should have raised a NotAPropertyError")
        except NotAPropertyError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAPropertyError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            get_property(file_path=pathToValidJSON, keys=invalidKeys)
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    @parameterized.expand(simpleTypeKeys)
    def test_returnsSimpleJSONPropertiesCorrectly(self, key: str):
        self.assertTrue(expr=validJSONData[key] == get_property(file_path=pathToValidJSON, keys=(key,)),
                        msg="getProperty return wrong value")

    def test_returnsJSONArrayCorrectly(self):
        self.assertTrue(expr=validJSONData[arrayKey] == get_property(file_path=pathToValidJSON, keys=(arrayKey,)),
                        msg="getProperty return wrong value")


class TestSuiteSetProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            set_property(file_path=pathToNoJSON, keys=(), value=None)
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            set_property(file_path=pathToInvalidJSON, keys=(), value=None)
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            set_property(file_path=pathToValidJSON, keys=(objectKey,), value=None)
            self.fail(msg="this should have raised a NotAPropertyError")
        except NotAPropertyError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAPropertyError")

    def test_raisesErrorIfNewValueNotAProperty(self):
        try:
            set_property(file_path=pathToValidJSON, keys=(arrayKey,), value=nonEmptyDict)
            self.fail(msg="this should have raised a NotAPropertyError")
        except NotAPropertyError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAPropertyError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            set_property(file_path=pathToValidJSON, keys=invalidKeys, value=None)
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    @parameterized.expand(list(simpleTypeKeysWithNewValues.keys()))
    def test_writesSimpleJSONPropertiesCorrectly(self, key: str):
        set_property(file_path=pathToValidJSON, keys=(key,), value=simpleTypeKeysWithNewValues[key])
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=simpleTypeKeysWithNewValues[key] == load(fp=fp)[key],
                            msg="after calling setProperty value is not written correctly to the file")

    def test_writesJSONArrayCorrectly(self):
        set_property(file_path=pathToValidJSON, keys=(arrayKey,), value=newArray)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=newArray == load(fp=fp)[arrayKey],
                            msg="after calling setProperty value is not written correctly to the file")


class TestSuiteAddProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            add_property(file_path=pathToNoJSON, keys=(), new_key="", value=None)
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            add_property(file_path=pathToInvalidJSON, keys=(), new_key="", value=None)
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_raisesErrorIfNotAProperty(self):
        try:
            add_property(file_path=pathToValidJSON, keys=(), new_key="", value=invalidJSONData)
            self.fail(msg="this should have raised a NotAPropertyError")
        except NotAPropertyError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAPropertyError")

    def test_raisesErrorIfParentObjectIsNoJSONObject(self):
        try:
            add_property(file_path=pathToValidJSON, keys=(arrayKey,), new_key="", value=newArray)
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            add_property(file_path=pathToValidJSON, keys=invalidKeys, new_key="", value=None)
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    def test_raisesErrorIfNewKeyAlreadyExists(self):
        try:
            add_property(file_path=pathToValidJSON, keys=(), new_key=arrayKey, value=None)
            self.fail(msg="this should have raised a JSONKeyAlreadyExists")
        except JSONKeyAlreadyExists:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyAlreadyExists")

    @parameterized.expand(mappedPythonTypes)
    def test_writesSimpleJSONPropertiesCorrectly(self, newVal: str):
        newKey = "newKey"
        add_property(file_path=pathToValidJSON, keys=(), new_key=newKey, value=newVal)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=newVal == load(fp=fp)[newKey],
                            msg="after calling addProperty the property is not written correctly in the json file")

    def test_writesArrayCorrectly(self):
        newKey = "newKey"
        add_property(file_path=pathToValidJSON, keys=(), new_key=newKey, value=newArray)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=newArray == load(fp=fp)[newKey],
                            msg="after calling addProperty the property is not written correctly in the json file")


class TestSuiteContainsProperty(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            contains_property(file_path=pathToNoJSON, keys=())
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            contains_property(file_path=pathToInvalidJSON, keys=())
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_falseIfKeysEmpty(self):
        self.assertFalse(expr=contains_property(file_path=pathToValidJSON, keys=()),
                         msg="containsProperty returned True for a empty key set")

    def test_falseIfPropertyDoesntExist(self):
        self.assertFalse(expr=contains_property(file_path=pathToValidJSON, keys=invalidKeys),
                         msg="containsProperty returned True for a property that doesn't exist")

    def test_falseIfKeysPointToObject(self):
        self.assertFalse(expr=contains_property(file_path=pathToValidJSON, keys=(objectKey,)),
                         msg="key set points to json object, but contains Property returned True")

    @parameterized.expand(simpleTypeKeys)
    def test_trueIfPropertyExists(self, key: str):
        self.assertTrue(expr=contains_property(file_path=pathToValidJSON, keys=(key,)),
                        msg=f"contains Property says that property '{(key,)}' doesn't exist but it does")


class TestSuiteGetObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            get_object(file_path=pathToNoJSON, keys=())
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            get_object(file_path=pathToInvalidJSON, keys=())
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    @parameterized.expand(simpleTypeKeys)
    def test_raisesErrorIfNotAObject(self, key: str):
        try:
            get_object(file_path=pathToValidJSON, keys=(key,))
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            get_object(file_path=pathToValidJSON, keys=invalidKeys)
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    def test_returnsJSONObjectCorrectly(self):
        self.assertTrue(expr=validJSONData[objectKey] == get_object(file_path=pathToValidJSON, keys=(objectKey,)),
                        msg="getObject return wrong value")


class TestSuiteSetObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            setObject(file_path=pathToNoJSON, keys=(), new_object={})
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            setObject(file_path=pathToInvalidJSON, keys=(), new_object={})
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    @parameterized.expand(simpleTypeKeys)
    def test_raisesErrorIfNotAObject(self, key: str):
        try:
            setObject(file_path=pathToValidJSON, keys=(key,), new_object={})
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_raisesErrorIfNewValueNotAObject(self):
        try:
            setObject(file_path=pathToValidJSON, keys=(objectKey,), new_object=newArray)
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            setObject(file_path=pathToValidJSON, keys=invalidKeys, new_object={})
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    def test_writesJSONObjectCorrectly(self):
        setObject(file_path=pathToValidJSON, keys=(objectKey,), new_object=nonEmptyDict)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=nonEmptyDict == load(fp=fp)[objectKey],
                            msg="after calling setObject object is not written correctly to the file")

    def test_writesEmptyJSONObjectCorrectly(self):
        setObject(file_path=pathToValidJSON, keys=(objectKey,), new_object=emptyDict)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=emptyDict == load(fp=fp)[objectKey],
                            msg="after calling setObject object is not written correctly to the file")


class TestSuiteAddObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            add_object(file_path=pathToNoJSON, keys=(), new_key="", new_object={})
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            add_object(file_path=pathToInvalidJSON, keys=(), new_key="", new_object={})
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_raisesErrorIfParentObjectIsNoJSONObject(self):
        try:
            add_object(file_path=pathToValidJSON, keys=(arrayKey,), new_key="", new_object=nonEmptyDict)
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    @parameterized.expand(mappedPythonTypes)
    def test_raisesErrorIfNotAObject(self, test_object: any):
        try:
            add_object(file_path=pathToValidJSON, keys=(), new_key="", new_object=test_object)
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_raisesErrorIfAKeyDoesNotExist(self):
        try:
            add_object(file_path=pathToValidJSON, keys=invalidKeys, new_key="", new_object={})
            self.fail(msg="this should have raised a JSONKeyNotFoundError")
        except JSONKeyNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyNotFoundError")

    def test_raisesErrorIfNewKeyAlreadyExists(self):
        try:
            add_object(file_path=pathToValidJSON, keys=(), new_key=objectKey, new_object={})
            self.fail(msg="this should have raised a JSONKeyAlreadyExists")
        except JSONKeyAlreadyExists:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONKeyAlreadyExists")

    def test_writesJSONObjectCorrectly(self):
        newKey = "newKey"
        add_object(file_path=pathToValidJSON, keys=(), new_key=newKey, new_object=nonEmptyDict)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=nonEmptyDict == load(fp=fp)[newKey],
                            msg="after calling addObject the property is not written correctly in the json file")

    def test_writesEmptyJSONObjectCorrectly(self):
        newKey = "newKey"
        add_object(file_path=pathToValidJSON, keys=(), new_key=newKey, new_object=emptyDict)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=emptyDict == load(fp=fp)[newKey],
                            msg="after calling addObject the property is not written correctly in the json file")


class TestSuiteContainsObject(SuperTestClass):

    def test_raisesErrorIfPathInvalid(self):
        try:
            contains_object(file_path=pathToNoJSON, keys=())
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfInvalidJSONInFile(self):
        try:
            contains_property(file_path=pathToInvalidJSON, keys=())
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_trueIfKeysEmpty(self):
        self.assertTrue(expr=contains_object(file_path=pathToValidJSON, keys=()),
                        msg="containsObject returned False for a empty key set")

    def test_falseIfObjectDoesntExist(self):
        self.assertFalse(expr=contains_object(file_path=pathToValidJSON, keys=invalidKeys),
                         msg="containsObject returned True for a object that doesn't exist")

    @parameterized.expand(simpleTypeKeys)
    def test_falseIfKeysPointToProperty(self, key: str):
        self.assertFalse(expr=contains_object(file_path=pathToValidJSON, keys=(key,)),
                         msg="key set points to json property, but containsObject returned True")

    def test_trueIfObjectExists(self):
        self.assertTrue(expr=contains_object(file_path=pathToValidJSON, keys=(objectKey,)),
                        msg=f"containsObject says that object '{(objectKey,)}' doesn't exist but it does")


if __name__ == "__main__":
    main()
