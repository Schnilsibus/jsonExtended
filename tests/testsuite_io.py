import sys
from unittest import main, TestCase
from pathlib import Path
from json import JSONDecodeError, load
from consts import *
sys.path.append("D:\Desktop\jsonExtended")
from _core.jsonx import *

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

class TestSuite_readJSONFile(TestCase):

    def setUp(self):
        globalSetUp(write = True)

    def tearDown(self):
        globalTearDown()

    def test_raisesErrorIfPathInvalid(self):
        try:
            readJSONFile(filePath = pathToNoJSON)
            self.fail("this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail("this should have raised a FileNotFoundError")

    def test_raisesErrorIfJSONFileInvalid(self):
        try:
            readJSONFile(filePath = pathToInvalidJSON)
            self.fail(msg = "this should have raised a JSONDecodeError")
        except JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a JSONDecodeError")

    def test_readDataEqualToFileContents(self):
        readData = readJSONFile(filePath = pathToValidJSON)
        self.assertTrue(expr = readData == validJSONData, msg = "read and decoded file contents are not correct")

class TestSuite_writeJSONFile(TestCase):
    
    def setUp(self):
        globalSetUp(write = False)

    def tearDown(self):
        globalTearDown()
    
    def test_raisesErrorIfPathInvalid(self):
        try:
            writeJSONFile(filePath = pathToNoJSON, data = validJSONData)
            self.fail(msg = "this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a FileNotFoundError")

    def test_raisesErrorIfDataNotJSONSerializable(self):
        try:
            writeJSONFile(filePath = pathToValidJSON, data = invalidJSONData)
            self.fail(msg = "this should have raised a TypeError")
        except TypeError as ex:
            pass
        except Exception as ex:
            self.fail(msg = "this should have raised a TypeError")

    def test_writtenDataEqualToInputData(self):
        writeJSONFile(filePath = pathToValidJSON, data = validJSONData)
        with open(file = pathToValidJSON, mode = "r") as fp:
            self.assertTrue(expr = validJSONData == load(fp = fp), msg = "written and encoded file contents are not correct")

class TestSuite_indentFile(TestCase):

    def setUp(self):
        globalSetUp(write = True)

    def tearDown(self):
        globalTearDown()
    
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

if (__name__ == "__main__"):
    main()