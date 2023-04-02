import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name = "jsonx",
    version = "0.0.1",
    author = "Nils Urbach",
    author_email = "ndu01u@gmail.com",
    description = "additional methods for handling json files in python",
    long_description = long_description,
    url = "https://github.com/Schnilsibus/jsonExtended.git",
    packages = setuptools.find_packages(where = "_core"),
    classifiers = [
    
    ]
)   