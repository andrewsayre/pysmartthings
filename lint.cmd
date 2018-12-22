@echo off
pip install isort --quiet
isort tests pysmartthings --recursive
pip install -r test-requirements.txt --quiet
pylint tests pysmartthings
flake8 tests pysmartthings
pydocstyle tests pysmartthings