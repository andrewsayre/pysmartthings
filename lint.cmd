@echo off
isort tests pysmartthings
black tests pysmartthings
pylint tests pysmartthings
flake8 tests pysmartthings
pydocstyle tests pysmartthings