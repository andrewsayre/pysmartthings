"""Tests for the SmartThings file."""

from pysmartthings import create
from pysmartthings.app import App
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
        apps = smartthings.apps()
        # assert
        assert len(apps) == 1

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
    def test_get_app_oauth(requests_mock):
        """Tests retrieval of OAuth settings."""
        # Arrange
        api_mock.setup(requests_mock)
        smartthings = SmartThings(api_mock.API_TOKEN)
        app_id = api_mock.APP_ID
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
        assert len(apps) == 1

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
