"""Tests for the Location file."""

import json
from pysmartthings.smartthings import Location


class TestLocation:
    """Tests for the Location class."""

    @staticmethod
    def test_initialize():
        """Tests whether the Device class initializes correctly."""
        # arrange
        with open("tests/json/location_test_home.json", "r") as json_file:
            entity = json.load(json_file)
        # act
        location = Location(None, entity)
        # assert
        assert location.name == "Test Home"
        assert location.location_id == "5c03e518-118a-44cb-85ad-7877d0b302e4"
