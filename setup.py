"""SmartThings Cloud API"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pysmartthings',
      version='0.1.1',
      description='A python library for interacting with the SmartThings cloud API.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/andrewsayre/pysmartthings',
      author='Andrew Sayre',
      author_email='andrew@sayre.net',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests'],
      tests_require=['tox'],
      platforms=['any'],
      keywords="smartthings",
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries",
          "Topic :: Home Automation",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          ])
