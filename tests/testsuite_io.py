from unittest import main, TestCase
from consts import *
from _core.json_extended import *


class TestSuiteReadJSONFile(TestCase):

    def setUp(self):
        globalSetUp(write=True)

    def tearDown(self):
        globalTearDown()

    def test_raisesErrorIfPathInvalid(self):
        try:
            read_json_file(file_path=pathToNoJSON)
            self.fail("this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail("this should have raised a FileNotFoundError")

    def test_raisesErrorIfJSONFileInvalid(self):
        try:
            read_json_file(file_path=pathToInvalidJSON)
            self.fail(msg="this should have raised a JSONDecodeError")
        except JSONDecodeError:
            pass
        except Exception:
            self.fail(msg="this should have raised a JSONDecodeError")

    def test_readDataEqualToFileContents(self):
        readData = read_json_file(file_path=pathToValidJSON)
        self.assertTrue(expr=readData == validJSONData, msg="read and decoded file contents are not correct")


class TestSuiteWriteJSONFile(TestCase):

    def setUp(self):
        globalSetUp(write=False)

    def tearDown(self):
        globalTearDown()

    def test_raisesErrorIfPathInvalid(self):
        try:
            write_json_file(file_path=pathToNoJSON, data=validJSONData)
            self.fail(msg="this should have raised a FileNotFoundError")
        except FileNotFoundError:
            pass
        except Exception:
            self.fail(msg="this should have raised a FileNotFoundError")

    def test_raisesErrorIfDataNotJSONSerializable(self):
        try:
            write_json_file(file_path=pathToValidJSON, data=invalidJSONData)
            self.fail(msg="this should have raised a NotAObjectError")
        except NotAObjectError:
            pass
        except Exception:
            self.fail(msg="this should have raised a NotAObjectError")

    def test_writtenDataEqualToInputData(self):
        write_json_file(file_path=pathToValidJSON, data=validJSONData)
        with open(file=pathToValidJSON, mode="r") as fp:
            self.assertTrue(expr=validJSONData == load(fp=fp), msg="written and encoded file contents are not correct")


if __name__ == "__main__":
    main()
