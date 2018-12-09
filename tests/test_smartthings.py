"""Tests for the SmartThings file."""

from pysmartthings.smartthings import SmartThings
from . import api_mock


class TestSmartThings:
    """Tests for the SmartThings class."""

    @staticmethod
    def test_devices(requests_mock):
        """Tests devices are retrieved"""
        # arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # act
        devices = smartthings.devices()
        # assert
        assert len(devices) == 4

    @staticmethod
    def test_locations(requests_mock):
        """Tests locations are retrieved."""
        # arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # act
        locations = smartthings.locations()
        # assert
        assert len(locations) == 2
