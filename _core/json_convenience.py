"""
Name
----
    json-convenience
Description
-----------
    This module extends the json module.
    Its core functionality is to get, set or add single json objects or properties from a json file,
    without manually loading and writing to the file and working with it's the dict representation.
    This could for example be used for configurations files o.ä.

Classes
-------
    no classes

Functions
-------
    read_json_file() - read the contents of a json file
    write_json_file() - write a dict to a json file
    is_format_correct() - check if a file contains valid json
    indent_json_file() - pretty indent a json file
    get_property() - get a specific property in a json file
    set_property() - set a specific property in a json file
    add_property() - add a specific property to a json file
    contains_property() - check if a json file contains a specific property
    get_object() - get a specific object in a json file
    set_object() - set a specific object in a json file
    add_object() - add a specific object to a json file
    contains_object() - check if a json file contains a specific object

Exceptions
----------
    NotAPropertyError - raised if a python/json object is not a (or not mapped to) a json property
    NotAObjectError - raised if a python/json object is not a (or not mapped to) a json object
    JSONKeyNotFoundError - raised if a json key is not found a file
    JSONKeyAlreadyExistsError - raised if a json key already exists & it is tried to add it to a file
"""

from json import dump, load, JSONDecodeError
from pathlib import Path
from typing import Any, Union, Tuple

_indent_level = 4

Property = Union[None, bool, int, float, str, list]
Object = dict


class NotAPropertyError(Exception):
    """
    An Error that is raised if a python object has a type that is not mapped to a json type

    Can also be raised if contents of a json file should be a json property but are a json object.
    json types that are called properties are: array, string, number, boolean, null.
    The python types that are mapped to those are: list, str, int, float, bool, None.
    Every other python type is not considered a json property.
    """

    def __init__(self, no_property_object: Any):
        """
        Parameters
        ----------
        no_property_object: Any
            the python object whose type is not mapped to a json property
        """

        Exception.__init__(
            self,
            f"the json object {no_property_object} is not a property; properties are: json data types and json arrays"
        )


class NotAObjectError(Exception):
    """
    An Error that is raised if a python object has a type that is not mapped to a json object

    Can also be raised if contents of a json file should be a json object but are a json property.
    json objects are the objects enclosed in curly braces in json files.
    The python type that is mapped to this is: dict.
    Every other python type is not considered a json object.
    """

    def __init__(self, no_object: Any):
        """
        Parameters
        ----------
        no_object: Any
            the python object whose type is not mapped to a json object
        """

        Exception.__init__(self, f"the json value {no_object} is not a json object")


class JSONKeyNotFoundError(Exception):
    """
    An Error that is raised if a key is not found in a json file
    """

    def __init__(self, wrong_key: str, all_keys_of_object: Tuple, found_keys: Tuple = None):
        """
        Parameters
        ----------
        wrong_key: str
            the key that could not be found
        all_keys_of_object: Tuple
            all the keys of the object in which the wrong key could not be found
        found_keys: Tuple (default=None)
            all the keys of the parent json objects of the object in which the wrong key could not be found
        """

        Exception.__init__(self,
                           f"key '{wrong_key}' not in {all_keys_of_object}; found keys: [{'->'.join(found_keys)}]")


class JSONKeyAlreadyExists(Exception):
    """
    An Error that is raised if a key already exists in a json object
    """

    def __init__(self, double_key: str, all_keys_of_object: Tuple, found_keys: Tuple = None):
        """
        Parameters
        ----------
        double_key: str
            the key that already exists
        all_keys_of_object: Tuple
            all the keys of the object that already contains the doubled key
        found_keys: Tuple
            all the keys of the parent json objects of the object that contains the doubled key
        """

        Exception.__init__(
            self,
            f"key '{double_key}' already exists in {all_keys_of_object}; found keys: [{'->'.join(found_keys)}]"
        )


def get_property(file_path: Path, keys: Tuple) -> Property:
    """
    Return a property in a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired property;
        the key of the property is the last element of the tuple

    Returns
    -------
    the specified property

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAPropertyError
        if keys point to a json object (not a json property)
    """

    raw_data = read_json_file(file_path=file_path)
    value = _get_value_of_keys(raw_data=raw_data, keys=keys)
    if _is_json_object(raw_data=value):
        raise NotAPropertyError(no_property_object=value)
    return value


def set_property(file_path: Path, keys: Tuple, value: Property) -> None:
    """
    Set a property in a json file to a value

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired property;
        the key of the property is the last element of the tuple
    value: Property (must be a python type that is mapped to json property)
        the new value of the property

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAPropertyError
        - if keys point to a json object (not a json property)
        - if type(value) is not mapped to a json property
    """

    raw_data = read_json_file(file_path=file_path)
    parent_object = _get_value_of_keys(raw_data=raw_data, keys=keys[:-1])
    if not _contains_key(raw_data=parent_object, key=keys[-1]):
        raise JSONKeyNotFoundError(wrong_key=keys[-1], all_keys_of_object=tuple(parent_object.keys()),
                                   found_keys=keys[:-1])
    elif _is_json_object(raw_data=parent_object[keys[-1]]):
        raise NotAPropertyError(no_property_object=parent_object[keys[-1]])
    elif not _is_json_property(raw_data=value):
        raise NotAPropertyError(no_property_object=value)
    parent_object[keys[-1]] = value
    write_json_file(file_path=file_path, data=raw_data)


def add_property(file_path: Path, keys: Tuple, new_key: str, value: Property) -> None:
    """
    Add a json property to a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file point to the json object that should contain the new property
    new_key: str
        the new key of the property
    value: Property (must be a python type that is mapped to json property)
        the value of the new property

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAObjectError
        if keys points to a json property instead of a json object (can't add a property to a property)
    NotAPropertyError
        if the type(value) is not mapped to a json property
    """

    raw_data = read_json_file(file_path=file_path)
    parent_object = _get_value_of_keys(raw_data=raw_data, keys=keys)
    if not _is_json_object(raw_data=parent_object):
        raise NotAObjectError(no_object=parent_object)
    elif _contains_key(raw_data=parent_object, key=new_key):
        raise JSONKeyAlreadyExists(double_key=new_key, all_keys_of_object=tuple(parent_object.keys()), found_keys=keys)
    elif not _is_json_property(raw_data=value):
        raise NotAPropertyError(no_property_object=value, )
    parent_object[new_key] = value
    write_json_file(file_path=file_path, data=raw_data)


def contains_property(file_path: Path, keys: Tuple) -> bool:
    """
    Check if a json file contains a specified property

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired property;
        the key of the property is the last element of the tuple
    
    Returns
    -------
    - True if the json file contains the specified property
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    """

    raw_data = read_json_file(file_path=file_path)
    try:
        value = _get_value_of_keys(raw_data=raw_data, keys=keys)
        return _is_json_property(raw_data=value)
    except JSONKeyNotFoundError:
        return False


def get_object(file_path: Path, keys: Tuple) -> Object:
    """
    Return an object in a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired object;
        the key of the object is the last element of the tuple

    Returns
    -------
    the specified object

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAObjectError
        if keys point to a json property (not a json object)
    """

    rawData = read_json_file(file_path=file_path)
    json_object = _get_value_of_keys(raw_data=rawData, keys=keys)
    if _is_json_property(raw_data=json_object):
        raise NotAObjectError(no_object=json_object)
    return json_object


def setObject(file_path: Path, keys: Tuple, new_object: Object) -> None:
    """
    Set an object in a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired object;
        the key of the object is the last element of the tuple
    new_object: dict
        the new value of the object

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAObjectError
        - if keys point to a json property (not a json object)
        - if not type(value) == dict 
    """

    rawData = read_json_file(file_path=file_path)
    parentObject = _get_value_of_keys(raw_data=rawData, keys=keys[:-1])
    if not _contains_key(raw_data=parentObject, key=keys[-1]):
        raise JSONKeyNotFoundError(wrong_key=keys[-1], all_keys_of_object=tuple(parentObject.keys()),
                                   found_keys=keys[:-1])
    elif _is_json_property(raw_data=parentObject[keys[-1]]):
        raise NotAObjectError(no_object=parentObject[keys[-1]])
    elif not _is_json_object(raw_data=new_object):
        raise NotAObjectError(no_object=new_object)
    parentObject[keys[-1]] = new_object
    write_json_file(file_path=file_path, data=rawData)


def add_object(file_path: Path, keys: Tuple, new_key: str, new_object: Object) -> None:
    """
    Add a json object to a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file point to the json object that should contain the new object
    new_key: str
        the new key of the object
    new_object: dict
        the new object

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    JSONKeyNotFoundError
        if keys contains a key that cannot be found (in the json object that the keys before the not-found-key point to)
    NotAObjectError
        - if keys points to a json property instead of a json object (can't add an object to a property)
        - if the type(value) is not mapped to a json object
    """

    rawData = read_json_file(file_path=file_path)
    parentObject = _get_value_of_keys(raw_data=rawData, keys=keys)
    if not _is_json_object(raw_data=parentObject):
        raise NotAObjectError(no_object=parentObject)
    elif _contains_key(raw_data=parentObject, key=new_key):
        raise JSONKeyAlreadyExists(double_key=new_key, all_keys_of_object=tuple(parentObject.keys()), found_keys=keys)
    elif not _is_json_object(raw_data=new_object):
        raise NotAObjectError(no_object=new_object)
    parentObject[new_key] = new_object
    write_json_file(file_path=file_path, data=rawData)


def contains_object(file_path: Path, keys: Tuple) -> bool:
    """
    Check if a json file contains a specified object

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    keys: Tuple
        the ordered! keys in the json file that contain the desired object;
        the key of the object is the last element of the tuple
    
    Returns
    -------
    - True if the json file contains the specified object
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    """

    rawData = read_json_file(file_path=file_path)
    try:
        value = _get_value_of_keys(raw_data=rawData, keys=keys)
        return _is_json_object(raw_data=value)
    except JSONKeyNotFoundError:
        return False


def is_format_correct(file_path: Path) -> bool:
    """
    Check if a file contains valid json

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the file

    Returns
    -------
    - True if the file contains valid json (== json.load() doesn't throw a json.JSONDecodeError)
    - False else

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    """

    try:
        read_json_file(file_path=file_path)
    except JSONDecodeError:
        return False
    return True


def indent_json_file(file_path: Path) -> None:
    f"""
    Indent a json file

    The file is indented using the json.dump() method with indent = {_indent_level}
    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json
    """

    write_json_file(file_path=file_path, data=read_json_file(file_path=file_path))


def read_json_file(file_path: Path) -> Object:
    """
    Read the contents of a json file and returns them as a dict

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file

    Returns
    -------
    The deserialized contents of a json file as a dict

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    json.JSONDecodeError
        if the file that filePath points to cannot be decoded by the json package ergo doesn't contain valid json 
    """

    if not file_path.exists():
        raise FileNotFoundError(f"the json file {file_path} doesn't exist")
    with file_path.open(mode="r") as fp:
        return load(fp=fp)


def write_json_file(file_path: Path, data: Object) -> None:
    """
    Write a dict to a json file

    Parameters
    ----------
    file_path: pathlib.Path
        the path to the json file
    data: dict
        the data that should be written to the json file
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if filePath doesn't point to a file
    NotAObjectError
        if not type(data) == dict 
    """

    if not file_path.exists():
        raise FileNotFoundError(f"the json file {file_path} doesn't exist")
    elif not _is_json_object(raw_data=data):
        raise NotAObjectError(no_object=data)
    with file_path.open(mode="w") as fp:
        dump(obj=data, fp=fp, indent=_indent_level)


def _get_value_of_keys(raw_data: dict, keys: Tuple) -> Union[Object, Property]:
    current_object = raw_data
    for i in range(len(keys)):
        if not _contains_key(raw_data=current_object, key=keys[i]):
            raise JSONKeyNotFoundError(wrong_key=keys[i],
                                       all_keys_of_object=tuple(raw_data.keys()),
                                       found_keys=keys[:i])
        current_object = current_object[keys[i]]
    return current_object


def _is_json_property(raw_data: Any) -> bool:
    return type(raw_data) in [type(None), float, int, list, bool, str]


def _is_json_object(raw_data: Any) -> bool:
    return type(raw_data) == dict


def _contains_key(raw_data: Object, key: str) -> bool:
    return key in raw_data.keys()
