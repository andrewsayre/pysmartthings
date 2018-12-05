@echo off
pip install -r test-requirements.txt --quiet
pylint pysmartthings
flake8 pysmartthings
pydocstyle pysmartthings