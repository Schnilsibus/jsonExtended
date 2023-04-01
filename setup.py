import setuptools

with open("README.md", "r") as fp
    long_description = fp.read()

setuptools.setup(
    name = "com.Schnilsibus.jsonExtended",
    version = "1.0.0",
    scripts = [
    
    ],
    author = "Nils D. Urbach",
    author_email = "ndu01u@gmail.com",
    description = "additional methods for handling json files in python",
    long_description = long_description,
    url = "",
    packages = setuptools.find_packages(),

)