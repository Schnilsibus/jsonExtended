import sys
import unittest
from pathlib import Path
import os
sys.path.append("D:\Desktop\jsonExtended")
import _core.jsonx as jsonx
from consts import *

def globalSetUp():
    with open(file = pathToValidJSON, mode = "w") as fp:
            fp.write(validJSONStr)
    with open(file = pathToInvalidJSON, mode = "w") as fp:
            fp.write(invalidJSONStr)

def globalTearDown():
    pathToValidJSON.unlink()
    pathToInvalidJSON.unlink()

class TestSuite_readJSONFile(unittest.TestCase):

    def setUp(self):
        globalSetUp()
        with open(file = pathToValidJSON, mode = "w") as fp:
            fp.write(validJSONStr)
        with open(file = pathToInvalidJSON, mode = "w") as fp:
            fp.write(invalidJSONStr)

    def tearDown(self):
        globalTearDown()

    def test_throwsErrorIfPathInvalid(self):
        try:
            jsonx._readJSONFile(filePath = pathToNoJSON)
            self.fail("this should have raised a FileNotFoundError")
        except FileNotFoundError as ex:
            pass
        except Exception as ex:
            self.fail("this should have raised a FileNotFoundError")

    def test_throwsErrorIfJSONFileInvalid(self):
        try:
            jsonx._readJSONFile(filePath = pathToInvalidJSON)
            self.fail("this should have raised a JSONDecodeError")
        except json.JSONDecodeError as ex:
            pass
        except Exception as ex:
            self.fail("this should have raised a JSONDecodeError")


    def test_readDataEqualToFileContents(self):
        readData = jsonx._readJSONFile(filePath = pathToValidJSON)
        self.assertTrue(expr = readData == validJSONData, msg = "decoded file contents are not correct")

    

class TestSuite_writeJSONFile(unittest.TestCase):
    pass

class TestSuite_indentFile(unittest.TestCase):
    pass



if (__name__ == "__main__"):
    unittest.main()