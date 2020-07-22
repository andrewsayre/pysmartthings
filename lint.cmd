@echo off
isort tests pysmartthings --recursive
black tests pysmartthings
pylint tests pysmartthings
flake8 tests pysmartthings
pydocstyle tests pysmartthings