@echo off
pip install -r test-requirements.txt --quiet
pylint tests pysmartthings
flake8 tests pysmartthings
pydocstyle tests pysmartthings