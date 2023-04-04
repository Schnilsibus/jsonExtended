import sys
import unittest
from pathlib import Path
import os
sys.path.append("D:\Desktop\jsonExtended")
import _core.jsonx as jsonx
from consts import *

def globalSetUp():
    open(file = validPath, mode = "x").close()
    open(file = invalidPath, mode = "x").close()

def globalTearDown():
    validPath.unlink()
    invalidPath.unlink()

class TestSuite_readJSONFile(unittest.TestCase):

    def setUp(self):
        globalSetUp()
        with open(file = validPath, mode = "w") as fp:
            fp.write(validJSONStr)
        with open(file = invalidPath, mode = "w") as fp:
            fp.write(invalidJSONStr)

    def tearDown(self):
        globalTearDown()

    def test_throwsErrorIfJSONFileInvalid(self):


    def test_readDataEqualToFileContents(self):
        with open(file = validPath, mode = "w") as fp:
            fp.write(validJSONStr)
        self.assertTrue(jsonx._readJSONFile(filePath = validPath) == validPath)

    

class TestSuite_writeJSONFile(unittest.TestCase):
    pass

class TestSuite_indentFile(unittest.TestCase):
    pass



if (__name__ == "__main__"):
    unittest.main()