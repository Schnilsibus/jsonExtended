import sys
import unittest
from pathlib import Path
sys.path.append("D:\Desktop\jsonExtended")
print("\n".join(sys.path))
import _core.jsonx as jsonx
import consts

class TestSuiteFileIO(unittest.TestCase):
    def some_test(self):
        try:
            raise NotADirectoryError()
        except Exception as e:
            raise NotADirectoryError()

if (__name__ == "__main__"):
    unittest.main()