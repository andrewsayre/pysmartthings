"""Tests for the SmartThings file."""

from pysmartthings.smartthings import SmartThings
from pysmartthings import create
from . import api_mock


class TestSmartThings:
    """Tests for the SmartThings class."""

    @staticmethod
    def test_create(requests_mock):
        """Tests the create method."""
        # Arrange
        api_mock.setup(requests_mock)
        # Act
        smartthings = create(api_mock.API_TOKEN)
        devices = smartthings.devices()
        # assert
        assert len(devices) == 4

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

    @staticmethod
    def test_apps(requests_mock):
        """Tests locations are retrieved."""
        # arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # act
        locations = smartthings.apps()
        # assert
        assert len(locations) == 1

    @staticmethod
    def test_create_app():
        """Tests the create app method."""
        # Arrange
        smartthings = SmartThings('')
        # Act
        app = smartthings.create_app()
        # Assert
        assert app
        assert not app.app_id
