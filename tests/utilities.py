"""Define the test utilities module."""

import json


def get_json(file):
    """Load a json file."""
    with open("tests/json/" + file, "r") as json_file:
        return json.load(json_file)
