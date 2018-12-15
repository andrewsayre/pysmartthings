"""Tests for the Location file."""

from pysmartthings.smartthings import Location

from .utilities import get_json


class TestLocation:
    """Tests for the Location class."""

    @staticmethod
    def test_initialize():
        """Tests whether the Device class initializes correctly."""
        # arrange
        entity = get_json('location_test_home.json')
        # act
        location = Location(None, entity)
        # assert
        assert location.name == "Test Home"
        assert location.location_id == "5c03e518-118a-44cb-85ad-7877d0b302e4"
