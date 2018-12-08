"""Tests for the SmartThings file."""

from pysmartthings.smartthings import SmartThings
from . import api_mock


class TestSmartThings:
    """Tests for the SmartThings class."""

    @staticmethod
    def test_devices(requests_mock):
        """Tests whether devices are populated correctly from the API."""
        # arrange
        api_mock.setup(requests_mock)
        # act
        smartthings = SmartThings(api_mock.API_TOKEN)
        # assert
        assert len(smartthings.locations) == 2
        assert len(smartthings.devices) == 4
