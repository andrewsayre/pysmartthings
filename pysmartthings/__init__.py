"""A python library for interacting with the SmartThings cloud API."""

from .smartthings import SmartThings

__title__ = "pysmartthings"
__version__ = "0.2.0"


def create(token):
    """Create an instance of the SmartThings API with the specified token."""
    return SmartThings(token)
