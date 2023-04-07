import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name = "extend-json",
    version = "0.0.1",
    author = "Nils Urbach",
    author_email = "ndu01u@gmail.com",
    description = "additional methods for handling json files in python",
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    keywords = [
        "json",
        "extended",
    ],
    url = "https://github.com/Schnilsibus/jsonExtended.git",
    package_dir = {"": "_core"},
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    test_suite = "tests",
)   