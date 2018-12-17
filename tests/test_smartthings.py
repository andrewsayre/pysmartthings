"""Tests for the SmartThings file."""

from pysmartthings.smartthings import SmartThings
from pysmartthings import create
from pysmartthings.oauth import OAuth
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

    @staticmethod
    def test_delete_app(requests_mock):
        """Tests the delete app method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act/Assert
        smartthings.delete_app('c6cde2b0-203e-44cf-a510-3b3ed4706996')
        # Assert

    @staticmethod
    def test_get_app_oauth(requests_mock):
        """Tests retrieval of OAuth settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = 'c6cde2b0-203e-44cf-a510-3b3ed4706996'
        # Act
        oauth = smartthings.get_app_oauth(app_id)
        # Assert
        assert oauth.app_id == app_id
        assert oauth.client_name == 'pysmartthings-test'
        assert oauth.scope == ['r:devices']

    @staticmethod
    def test_update_app_oauth(requests_mock):
        """Tests updating OAuth settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = 'c6cde2b0-203e-44cf-a510-3b3ed4706996'
        oauth = OAuth(app_id)
        oauth.client_name = 'pysmartthings-test'
        oauth.scope.append('r:devices')
        # Act
        oauth_entity = smartthings.update_app_oauth(oauth)
        # Assert
        assert oauth_entity.app_id == oauth.app_id
        assert oauth_entity.client_name == oauth.client_name
        assert oauth_entity.scope == oauth.scope
