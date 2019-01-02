"""Tests for the SmartThings file."""

import pytest

from pysmartthings import create
from pysmartthings.app import App, AppSettings
from pysmartthings.oauth import OAuth
from pysmartthings.smartthings import SmartThings
from pysmartthings.subscription import Subscription

from . import api_mock
from .utilities import get_json


class TestSmartThings:
    """Tests for the SmartThings class."""

    @staticmethod
    def test_create(requests_mock):
        """Tests the create method."""
        # Arrange
        api_mock.setup(requests_mock)
        # Act
        smartthings = create(api_mock.API_TOKEN)
        # assert
        assert smartthings

    @staticmethod
    @pytest.mark.asyncio
    async def test_devices(smartthings):
        """Tests devices are retrieved."""
        # Act
        devices = await smartthings.devices()
        # Assert
        assert len(devices) == 4

    @staticmethod
    @pytest.mark.asyncio
    async def test_devices_with_filter(smartthings):
        """Tests retrieving a filtered view of devices."""
        # Act
        devices = await smartthings.devices(
            location_ids=[api_mock.LOCATION_ID],
            capabilities=['switch'],
            device_ids=['edd26ac6-d156-4505-9647-3b20118ae4d1',
                        'be1a61ce-c2a4-4b32-bf8c-31de6d3fa7dd'])
        # Assert
        assert len(devices) == 2

    @staticmethod
    @pytest.mark.asyncio
    async def test_device(smartthings):
        """Tests the device(id) method."""
        # Act
        device = await smartthings.device(api_mock.DEVICE_ID)
        # Assert
        assert device.device_id == api_mock.DEVICE_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_locations(smartthings):
        """Tests locations are retrieved."""
        # Act
        locations = await smartthings.locations()
        # Assert
        assert len(locations) == 2

    @staticmethod
    @pytest.mark.asyncio
    async def test_location(smartthings):
        """Tests the location(id) method."""
        # Act
        location = await smartthings.location(api_mock.LOCATION_ID)
        # Assert
        assert location.location_id == api_mock.LOCATION_ID

    @staticmethod
    def test_apps(requests_mock):
        """Tests locations are retrieved."""
        # arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # act
        apps = smartthings.apps()
        # assert
        assert len(apps) == 1

    @staticmethod
    def test_app(requests_mock):
        """Tests the app(id) method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        app = smartthings.app(api_mock.APP_ID)
        # Assert
        assert app.app_id == api_mock.APP_ID

    @staticmethod
    def test_create_app(requests_mock):
        """Tests the create app method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app = App()
        data = get_json('app_post_request.json')
        data['appId'] = api_mock.APP_ID
        app.apply_data(data)
        # Act
        app, oauth = smartthings.create_app(app)
        # Assert
        assert app.app_id == api_mock.APP_ID
        assert oauth.client_id == '7cd4d474-7b36-4e03-bbdb-4cd4ae45a2be'
        assert oauth.client_secret == '9b3fd445-42d6-441b-b386-99ea51e13cb0'

    @staticmethod
    def test_delete_app(requests_mock):
        """Tests the delete app method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act/Assert
        result = smartthings.delete_app(api_mock.APP_ID)
        # Assert
        assert result

    @staticmethod
    def test_app_settings(requests_mock):
        """Tests retrieval of app settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = api_mock.APP_ID
        # Act
        settings = smartthings.app_settings(app_id)
        # Assert
        assert settings.app_id == app_id
        assert settings.settings == {'test': 'test'}

    @staticmethod
    def test_update_app_settings(requests_mock):
        """Tests updating app settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = api_mock.APP_ID
        settings = AppSettings(app_id)
        settings.settings['test'] = 'test'
        # Act
        entity = smartthings.update_app_settings(settings)
        # Assert
        assert entity.app_id == settings.app_id
        assert entity.settings == {'test': 'test'}

    @staticmethod
    def test_app_oauth(requests_mock):
        """Tests retrieval of OAuth settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = api_mock.APP_ID
        # Act
        oauth = smartthings.app_oauth(app_id)
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
        app_id = api_mock.APP_ID
        oauth = OAuth(app_id)
        oauth.client_name = 'pysmartthings-test'
        oauth.scope.append('r:devices')
        # Act
        oauth_entity = smartthings.update_app_oauth(oauth)
        # Assert
        assert oauth_entity.app_id == oauth.app_id
        assert oauth_entity.client_name == oauth.client_name
        assert oauth_entity.scope == oauth.scope

    @staticmethod
    def test_installedapps(requests_mock):
        """Tests the installedapps method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        apps = smartthings.installedapps()
        # Assert
        assert len(apps) == 2

    @staticmethod
    def test_installedapp(requests_mock):
        """Tests the installedapp(id) method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        app = smartthings.installedapp(api_mock.INSTALLED_APP_ID)
        # Assert
        assert app.installed_app_id == api_mock.INSTALLED_APP_ID

    @staticmethod
    def test_delete_installedapp(requests_mock):
        """Tests the delete app method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act/Assert
        result = smartthings.delete_installedapp(api_mock.INSTALLED_APP_ID)
        # Assert
        assert result

    @staticmethod
    def test_subscriptions(requests_mock):
        """Tests the get subscriptions method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        subscriptions = smartthings.subscriptions(api_mock.INSTALLED_APP_ID)
        # Assert
        assert len(subscriptions) == 3

    @staticmethod
    def test_delete_subscriptions(requests_mock):
        """Tests the delete subscriptions method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        count = smartthings.delete_subscriptions(api_mock.INSTALLED_APP_ID)
        # Assert
        assert count == 3

    @staticmethod
    def test_delete_subscription(requests_mock):
        """Tests the delete subscription method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        # Act
        deleted = smartthings.delete_subscription(
            api_mock.INSTALLED_APP_ID, api_mock.SUBSCRIPTION_ID)
        # Assert
        assert deleted

    @staticmethod
    def test_create_subscription(requests_mock):
        """Tests the create subscription method."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        sub = Subscription()
        sub.source_type = 'CAPABILITY'
        sub.location_id = api_mock.LOCATION_ID
        sub.capability = 'switch'
        sub.installed_app_id = api_mock.INSTALLED_APP_ID
        # Act
        entity = smartthings.create_subscription(sub)
        # Assert
        assert entity.subscription_id == api_mock.SUBSCRIPTION_ID
