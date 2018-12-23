"""Tests for the Device file."""

import pytest

from pysmartthings.api import API
from pysmartthings.device import Device, DeviceEntity, DeviceStatus, DeviceType

from . import api_mock
from .utilities import get_json


class TestDevice:
    """Tests for the Device class."""

    @staticmethod
    def test_init():
        """Tests whether the Device class initializes correctly."""
        # Arrange/Act
        device = Device()
        # Assert
        assert device.type == DeviceType.UNKNOWN
        assert device.capabilities == []
        assert device.components == {}

    @staticmethod
    def test_apply_data():
        """Tests the apply data method."""
        # Arrange
        data = get_json('device.json')
        device = Device()
        # Act
        device.apply_data(data)
        # Assert
        assert device.device_id == api_mock.DEVICE_ID
        assert device.name == 'GE In-Wall Smart Dimmer'
        assert device.label == 'Front Porch Lights'
        assert device.location_id == api_mock.LOCATION_ID
        assert device.type is DeviceType.DTH
        assert device.device_type_id == '8a9d4b1e3b9b1fe3013b9b206a7f000d'
        assert device.device_type_name == 'Dimmer Switch'
        assert device.device_type_network == 'ZWAVE'
        assert device.capabilities == [
            'switch', 'switchLevel', 'refresh', 'indicator', 'sensor',
            'actuator', 'healthCheck', 'light']
        assert device.components == {
            "main": [
                'switch', 'switchLevel', 'refresh', 'indicator', 'sensor',
                'actuator', 'healthCheck', 'light']
        }


class TestDeviceEntity:
    """Tests for the DeviceEntity class."""

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        app.refresh()
        # Assert
        assert app.label == 'Front Porch Lights'

    @staticmethod
    def test_save():
        """Tests the save method."""
        # Arrange
        api = API(api_mock.API_TOKEN)
        app = DeviceEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            app.save()

    @staticmethod
    def test_switch_on(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = app.switch_on()
        # Assert
        assert result

    @staticmethod
    def test_switch_off(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = app.switch_off()
        # Assert
        assert result

    @staticmethod
    def test_set_level(requests_mock):
        """Tests the set_level method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = app.set_level(75, 2)
        # Assert
        assert result

    @staticmethod
    def test_status():
        """Tests the set_level method."""
        # Arrange
        app = DeviceEntity(None, device_id=api_mock.DEVICE_ID)
        # Act
        status = app.status
        # Assert
        assert status.device_id == api_mock.DEVICE_ID


class TestDeviceStatus:
    """Tests for the DeviceStatus class."""

    @staticmethod
    def test_init():
        """Tests the init method."""
        # Arrange/Act
        status = DeviceStatus(None, device_id=api_mock.DEVICE_ID)
        # Assert
        assert status.device_id == api_mock.DEVICE_ID
        assert status.attributes == {}
        assert not status.switch
        assert not status.motion
        assert status.level == 0

    @staticmethod
    def test_apply_data():
        """Tests the apply_data method."""
        # Arrange
        data = get_json('device_status.json')
        # Act
        status = DeviceStatus(None, api_mock.DEVICE_ID, data)
        # Assert
        assert len(status.attributes) == 9
        assert status.switch
        assert status.level == 100

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        status = DeviceStatus(api, device_id=api_mock.DEVICE_ID)
        # Act
        status.refresh()
        # Assert
        assert len(status.attributes) == 9
