"""SmartThings Cloud API"""

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join("README.md"), "r") as fh:
    long_description = fh.read()

const = {}
with open(os.path.join("pysmartthings", "const.py"), "r") as fp:
    exec(fp.read(), const)

setup(
    name=const["__title__"],
    version=const["__version__"],
    description="A python library for interacting with the SmartThings cloud API build with asyncio and aiohttp.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewsayre/pysmartthings",
    author="Andrew Sayre",
    author_email="andrew@sayre.net",
    license="ASL 2.0",
    packages=find_packages(exclude=("tests*",)),
    install_requires=["aiohttp>=3.5.1,<4.0.0"],
    tests_require=["tox>=3.5.0,<4.0.0"],
    platforms=["any"],
    keywords="smartthings",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
