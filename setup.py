import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name = "jsonx",
    version = "0.0.0",
    author = "Nils Urbach",
    author_email = "ndu01u@gmail.com",
    description = "additional methods for handling json files in python",
    long_description = long_description,
    keywords = [
        "json",
        "extended",
    ],
    url = "https://github.com/Schnilsibus/jsonExtended.git",
    package_dir = {"": "_core"},
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    install_requires = [
        "json",
        "pathlib",
    ],
    test_suite = "tests",
    tests_require = [
        "sys",
    ]
)   