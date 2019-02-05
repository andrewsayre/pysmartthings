"""Tests for the SmartThings file."""

import pytest

from pysmartthings.app import App, AppOAuth, AppSettings
from pysmartthings.room import Room
from pysmartthings.subscription import Subscription

from .conftest import (
    APP_ID, DEVICE_ID, INSTALLED_APP_ID, LOCATION_ID, ROOM_ID, SCENE_ID,
    SUBSCRIPTION_ID)
from .utilities import get_json


class TestSmartThings:
    """Tests for the SmartThings class."""

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
            location_ids=[LOCATION_ID],
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
        device = await smartthings.device(DEVICE_ID)
        # Assert
        assert device.device_id == DEVICE_ID

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
        location = await smartthings.location(LOCATION_ID)
        # Assert
        assert location.location_id == LOCATION_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_rooms(smartthings):
        """Tests the rooms(id) method."""
        # Act
        rooms = await smartthings.rooms(LOCATION_ID)
        # Assert
        assert len(rooms) == 1

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_room(smartthings):
        """Tests the create room method."""
        # Arrange
        room = Room()
        room.name = 'Theater'
        room.background_image = 'Test'
        room.location_id = LOCATION_ID
        # Act
        room = await smartthings.create_room(room)
        # Assert
        assert room.room_id == ROOM_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_room(smartthings):
        """Tests the create room method."""
        # Arrange
        room = Room()
        room.name = 'Theater'
        room.background_image = 'Test'
        room.location_id = LOCATION_ID
        room.room_id = ROOM_ID
        # Act
        room = await smartthings.update_room(room)
        # Assert
        assert room.room_id == ROOM_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_room(smartthings):
        """Tests the room(id, id) method."""
        # Act
        room = await smartthings.room(LOCATION_ID, ROOM_ID)
        # Assert
        assert room.room_id == ROOM_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_room(smartthings):
        """Tests the delete room."""
        # Act
        result = await smartthings.delete_room(LOCATION_ID, ROOM_ID)
        # Assert
        assert result

    @staticmethod
    @pytest.mark.asyncio
    async def test_apps(smartthings):
        """Tests locations are retrieved."""
        # Act
        apps = await smartthings.apps()
        # assert
        assert len(apps) == 1

    @staticmethod
    @pytest.mark.asyncio
    async def test_app(smartthings):
        """Tests the app(id) method."""
        # Act
        app = await smartthings.app(APP_ID)
        # Assert
        assert app.app_id == APP_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_app(smartthings):
        """Tests the create app method."""
        # Arrange
        app = App()
        data = get_json('app_post_request.json')
        data['appId'] = APP_ID
        app.apply_data(data)
        # Act
        app, oauth = await smartthings.create_app(app)
        # Assert
        assert app.app_id == APP_ID
        assert oauth.client_id == '7cd4d474-7b36-4e03-bbdb-4cd4ae45a2be'
        assert oauth.client_secret == '9b3fd445-42d6-441b-b386-99ea51e13cb0'

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_app(smartthings):
        """Tests the delete app method."""
        # Act/Assert
        result = await smartthings.delete_app(APP_ID)
        # Assert
        assert result

    @staticmethod
    @pytest.mark.asyncio
    async def test_app_settings(smartthings):
        """Tests retrieval of app settings."""
        # Act
        settings = await smartthings.app_settings(APP_ID)
        # Assert
        assert settings.app_id == APP_ID
        assert settings.settings == {'test': 'test'}

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_app_settings(smartthings):
        """Tests updating app settings."""
        # Arrange
        settings = AppSettings(APP_ID)
        settings.settings['test'] = 'test'
        # Act
        entity = await smartthings.update_app_settings(settings)
        # Assert
        assert entity.app_id == settings.app_id
        assert entity.settings == {'test': 'test'}

    @staticmethod
    @pytest.mark.asyncio
    async def test_app_oauth(smartthings):
        """Tests retrieval of OAuth settings."""
        # Act
        oauth = await smartthings.app_oauth(APP_ID)
        # Assert
        assert oauth.app_id == APP_ID
        assert oauth.client_name == 'pysmartthings-test'
        assert oauth.scope == ['r:devices']

    @staticmethod
    @pytest.mark.asyncio
    async def test_update_app_oauth(smartthings):
        """Tests updating OAuth settings."""
        # Arrange
        oauth = AppOAuth(APP_ID)
        oauth.client_name = 'pysmartthings-test'
        oauth.scope.append('r:devices')
        # Act
        oauth_entity = await smartthings.update_app_oauth(oauth)
        # Assert
        assert oauth_entity.app_id == oauth.app_id
        assert oauth_entity.client_name == oauth.client_name
        assert oauth_entity.scope == oauth.scope

    @staticmethod
    @pytest.mark.asyncio
    async def test_installed_apps(smartthings):
        """Tests the installedapps method."""
        # Act
        apps = await smartthings.installed_apps()
        # Assert
        assert len(apps) == 2

    @staticmethod
    @pytest.mark.asyncio
    async def test_installed_app(smartthings):
        """Tests the installedapp(id) method."""
        # Act
        app = await smartthings.installed_app(INSTALLED_APP_ID)
        # Assert
        assert app.installed_app_id == INSTALLED_APP_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_installed_app(smartthings):
        """Tests the delete app method."""
        # Act/Assert
        result = await smartthings.delete_installed_app(
            INSTALLED_APP_ID)
        # Assert
        assert result

    @staticmethod
    @pytest.mark.asyncio
    async def test_subscriptions(smartthings):
        """Tests the get subscriptions method."""
        # Act
        subscriptions = await smartthings.subscriptions(INSTALLED_APP_ID)
        # Assert
        assert len(subscriptions) == 3

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_subscriptions(smartthings):
        """Tests the delete subscriptions method."""
        # Act
        count = await smartthings.delete_subscriptions(INSTALLED_APP_ID)
        # Assert
        assert count == 3

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_subscription(smartthings):
        """Tests the delete subscription method."""
        # Act
        deleted = await smartthings.delete_subscription(
            INSTALLED_APP_ID, SUBSCRIPTION_ID)
        # Assert
        assert deleted

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_subscription(smartthings):
        """Tests the create subscription method."""
        # Arrange
        sub = Subscription()
        sub.source_type = 'CAPABILITY'
        sub.location_id = LOCATION_ID
        sub.capability = 'switch'
        sub.installed_app_id = INSTALLED_APP_ID
        # Act
        entity = await smartthings.create_subscription(sub)
        # Assert
        assert entity.subscription_id == SUBSCRIPTION_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_scenes(smartthings):
        """Tests the scenes method."""
        # Act
        scenes = await smartthings.scenes()
        # Assert
        assert len(scenes) == 2

    @staticmethod
    @pytest.mark.asyncio
    async def test_scenes_with_location_filter(smartthings):
        """Tests the scenes method."""
        # Act
        scenes = await smartthings.scenes(location_id=LOCATION_ID)
        # Assert
        assert len(scenes) == 1

    @staticmethod
    @pytest.mark.asyncio
    async def test_execute_scene(smartthings):
        """Tests the execute scene method."""
        # Act
        result = await smartthings.execute_scene(SCENE_ID)
        # Assert
        assert result
