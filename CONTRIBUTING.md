# Contributing Guidelines

Contributions welcome!

**Before spending lots of time on something, ask for feedback on your idea first!**

## Style

This repository follows [PEP8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257 (Docstring Conventions)](https://www.python.org/dev/peps/pep-0257/).  Imports should be sorted with `isort`.  Commits and pull requests are automatically linted with Coveralls, Travis CI, and Hound.

*Save time by checking for style/lint issues **before** committing.*  Run `lint.bat` to automatically install the test dependencies and run the linters.  Alternatively, you can run the linters manually from the root of the project:
```bash
pip install isort
pip install -r test-requirements.txt

isort tests pysmartthings --recursive
pylint tests pysmartthings
flake8 tests pysmartthings
pydocstyle tests pysmartthings
```

## Testing

All code is checked to verify:
- All the unit tests pass
- All code passes the checks from the linting tools
- Code coverage is maintained or improved without adding exclusions to `.coveragerc`

You can run all the tests with Tox in a virtual environment by simply running:
```bash
tox
```

Unit tests can be ran outside of Tox by running:
```bash
pytest tests
```

To check the code coverage and determine which statements are not covered, run:
```bash
pytest tests --cov --cov-report=term-missing
```

### Rules

There are a few basic ground-rules for contributors:
1. Follow the style and testing guidelines above
2. Fill out the pull request template and complete check-list activities
3. Submit a pull request and be responsive to questions and feedback

### Releases

Declaring formal releases remains the prerogative of the project maintainer.

### Changes to this arrangement

This is an experiment and feedback is welcome! This document may also be subject to pull-
requests or changes by contributors where you believe you have something valuable to add
or change.

## Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

- (a) The contribution was created in whole or in part by me and I have the right to
  submit it under the open source license indicated in the file; or

- (b) The contribution is based upon previous work that, to the best of my knowledge, is
  covered under an appropriate open source license and I have the right under that license
  to submit that work with modifications, whether created in whole or in part by me, under
  the same open source license (unless I am permitted to submit under a different
  license), as indicated in the file; or

- (c) The contribution was provided directly to me by some other person who certified
  (a), (b) or (c) and I have not modified it.

- (d) I understand and agree that this project and the contribution are public and that a
  record of the contribution (including all personal information I submit with it,
  including my sign-off) is maintained indefinitely and may be redistributed consistent
  with this project or the open source license(s) involved.