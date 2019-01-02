"""Tests for the Device file."""

import pytest

from pysmartthings.api import api_old
from pysmartthings.device import (
    Attribute, Device, DeviceEntity, DeviceStatus, DeviceType)

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
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        device.refresh()
        # Assert
        assert device.label == 'Front Porch Lights'

    @staticmethod
    def test_save():
        """Tests the save method."""
        # Arrange
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            device.save()

    @staticmethod
    def test_switch_on(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = device.switch_on()
        # Assert
        assert result
        assert not device.status.switch

    @staticmethod
    def test_switch_on_update(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = device.switch_on(True)
        # Assert
        assert result
        assert device.status.switch

    @staticmethod
    def test_switch_off(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        device.status.switch = True
        # Act
        result = device.switch_off()
        # Assert
        assert result
        assert device.status.switch

    @staticmethod
    def test_switch_off_update(requests_mock):
        """Tests the switch_on method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        device.status.switch = True
        # Act
        result = device.switch_off(True)
        # Assert
        assert result
        assert not device.status.switch

    @staticmethod
    def test_set_level(requests_mock):
        """Tests the set_level method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = device.set_level(75, 2)
        # Assert
        assert result
        assert device.status.level == 0

    @staticmethod
    def test_set_level_update(requests_mock):
        """Tests the set_level method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        device = DeviceEntity(api, device_id=api_mock.DEVICE_ID)
        # Act
        result = device.set_level(75, 2, True)
        # Assert
        assert result
        assert device.status.level == 75

    @staticmethod
    def test_status():
        """Tests the set_level method."""
        # Arrange
        device = DeviceEntity(None, device_id=api_mock.DEVICE_ID)
        # Act
        status = device.status
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
    def test_apply_attribute_update():
        """Tests the apply_attribute_update method."""
        # Arrange
        data = get_json('device_status.json')
        status = DeviceStatus(None, api_mock.DEVICE_ID, data)
        # Act
        status.apply_attribute_update('main', 'switchLevel', 'level', 50)
        # Assert
        assert status.level == 50

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = api_old(api_mock.API_TOKEN)
        status = DeviceStatus(api, device_id=api_mock.DEVICE_ID)
        # Act
        status.refresh()
        # Assert
        assert len(status.attributes) == 9

    @staticmethod
    def test_switch():
        """Tests the init method."""
        # Arrange
        status = DeviceStatus(None, device_id=api_mock.DEVICE_ID)
        # Act
        status.switch = True
        # Assert
        assert status.switch

    @staticmethod
    def test_level():
        """Tests the init method."""
        # Arrange
        status = DeviceStatus(None, device_id=api_mock.DEVICE_ID)
        # Act
        status.level = 50
        # Assert
        assert status.level == 50

    @staticmethod
    def test_is_on():
        """Tests the is_on method."""
        # Arrange
        status = DeviceStatus(None, device_id=api_mock.DEVICE_ID)
        status.attributes[Attribute.acceleration] = 'active'
        status.attributes[Attribute.level] = 100
        # Act/Assert
        assert status.is_on(Attribute.acceleration)
        assert status.is_on(Attribute.level)
        assert not status.is_on(Attribute.switch)
