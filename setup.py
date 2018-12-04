"""SmartThings Cloud API"""
from setuptools import find_packages, setup

setup(name='pysmartthings',
      version='0.1.0',
      description='A python library for interacting with the SmartThings cloud API.',
      long_description='A python library for interacting with the SmartThings cloud API.',
      url='https://github.com/andrewsayre/pysmartthings',
      author='Andrew Sayre',
      author_email='andrew@sayre.net',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests'],
      tests_require=['tox'],
      platforms=['any'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries",
          "Topic :: Home Automation",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          ])
