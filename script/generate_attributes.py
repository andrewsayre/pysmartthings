#!/usr/bin/env python3
"""Generate capabilitiy constants."""
import re
import sys

sys.path.append(".")
from pysmartthings.capability import ATTRIBUTES


def main():
    """Run the script."""
    attribs = [a for a in ATTRIBUTES]
    attribs.sort()
    for a in attribs:
        print("{} = '{}'".format(re.sub(r'([A-Z])', r'_\1', a).lower(), a))


if __name__ == '__main__':
    sys.exit(main())
