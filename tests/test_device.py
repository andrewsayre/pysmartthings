"""Tests for the Device file."""

import pytest

from pysmartthings.device import (
    Attribute, Device, DeviceEntity, DeviceStatus, DeviceType)

from .conftest import DEVICE_ID, LOCATION_ID
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
        assert device.device_id == DEVICE_ID
        assert device.name == 'GE In-Wall Smart Dimmer'
        assert device.label == 'Front Porch Lights'
        assert device.location_id == LOCATION_ID
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
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        await device.refresh()
        # Assert
        assert device.label == 'Front Porch Lights'

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the save method."""
        # Arrange
        device = DeviceEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            await device.save()

    @staticmethod
    @pytest.mark.asyncio
    async def test_switch_on(api):
        """Tests the switch_on method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.switch_on()
        # Assert
        assert result
        assert not device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_switch_on_update(api):
        """Tests the switch_on method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.switch_on(True)
        # Assert
        assert result
        assert device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_switch_off(api):
        """Tests the switch_on method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.status.switch = True
        # Act
        result = await device.switch_off()
        # Assert
        assert result
        assert device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_switch_off_update(api):
        """Tests the switch_on method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.status.switch = True
        # Act
        result = await device.switch_off(True)
        # Assert
        assert result
        assert not device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_level(api):
        """Tests the set_level method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_level(75, 2)
        # Assert
        assert result
        assert device.status.level == 0
        assert not device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_level_invalid(api):
        """Tests the set_level method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert level
        levels = [-1, 101]
        for level in levels:
            with pytest.raises(ValueError):
                await device.set_level(level)
        # Assert duration
        with pytest.raises(ValueError):
            await device.set_level(100, -1)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_level_update(api):
        """Tests the set_level method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_level(75, 2, True)
        # Assert
        assert result
        assert device.status.level == 75
        assert device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_fan_speed(api):
        """Tests the set_fan_speed method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_fan_speed(66)
        # Assert
        assert result
        assert device.status.level == 0
        assert not device.status.switch

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_fan_speed_invalid(api):
        """Tests the set_fan_speed method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert
        with pytest.raises(ValueError):
            await device.set_fan_speed(-1)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_fan_speed_update(api):
        """Tests the set_fan_speed method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_fan_speed(66, True)
        # Assert
        assert result
        assert device.status.fan_speed == 66
        assert device.status.switch

    @staticmethod
    def test_status():
        """Tests the set_level method."""
        # Arrange
        device = DeviceEntity(None, device_id=DEVICE_ID)
        # Act
        status = device.status
        # Assert
        assert status.device_id == DEVICE_ID

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_temperature(api):
        """Tests the set_color_temperature method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color_temperature(3000)
        # Assert
        assert result
        assert device.status.color_temperature == 1

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_temperature_invalid(api):
        """Tests the set_color_temperature method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        values = [0, 30001]
        for value in values:
            with pytest.raises(ValueError):
                await device.set_color_temperature(value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_temperature_update(api):
        """Tests the set_color_temperature method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color_temperature(3000, True)
        # Assert
        assert result
        assert device.status.color_temperature == 3000

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_hue(api):
        """Tests the set_hue method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_hue(75)
        # Assert
        assert result
        assert device.status.hue == 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_hue_invalid(api):
        """Tests the set_hue method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert
        levels = [-1, 101]
        for level in levels:
            with pytest.raises(ValueError):
                await device.set_hue(level)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_hue_update(api):
        """Tests the set_hue method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_hue(75, True)
        # Assert
        assert result
        assert device.status.hue == 75

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_saturation(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_saturation(75)
        # Assert
        assert result
        assert device.status.saturation == 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_saturation_invalid(api):
        """Tests the set_saturation method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert
        levels = [-1, 101]
        for level in levels:
            with pytest.raises(ValueError):
                await device.set_saturation(level)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_saturation_update(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_saturation(75, True)
        # Assert
        assert result
        assert device.status.saturation == 75

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color(api):
        """Tests the set_color method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color(25, 50)
        # Assert
        assert result
        assert device.status.hue == 0
        assert device.status.saturation == 0
        assert device.status.color is None

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_invalid(api):
        """Tests the set_saturation method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert
        values = [-1, 101]
        for value in values:
            with pytest.raises(ValueError):
                await device.set_color(value, 0)
            with pytest.raises(ValueError):
                await device.set_color(0, value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_update(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color(25, 50, set_status=True)
        # Assert
        assert result
        assert device.status.hue == 25
        assert device.status.saturation == 50
        assert device.status.color == '#4B6432'

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_hex(api):
        """Tests the set_color method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color(color_hex='#4B6432')
        # Assert
        assert result
        assert device.status.hue == 0
        assert device.status.saturation == 0
        assert device.status.color is None

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_hex_invalid(api):
        """Tests the set_color method invalid values."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Assert
        values = ['000000', '#00000', '#G00000']
        for value in values:
            with pytest.raises(ValueError):
                await device.set_color(color_hex=value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_update_hex(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color(color_hex='#4B6432', set_status=True)
        # Assert
        assert result
        assert device.status.hue == 25
        assert device.status.saturation == 50
        assert device.status.color == '#4B6432'


class TestDeviceStatus:
    """Tests for the DeviceStatus class."""

    @staticmethod
    def test_init():
        """Tests the init method."""
        # Arrange/Act
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Assert
        assert status.device_id == DEVICE_ID
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
        status = DeviceStatus(None, DEVICE_ID, data)
        # Assert
        assert len(status.attributes) == 9
        assert status.switch
        assert status.level == 100

    @staticmethod
    def test_apply_attribute_update():
        """Tests the apply_attribute_update method."""
        # Arrange
        data = get_json('device_status.json')
        status = DeviceStatus(None, DEVICE_ID, data)
        # Act
        status.apply_attribute_update('main', 'switchLevel', 'level', 50)
        # Assert
        assert status.level == 50

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        status = DeviceStatus(api, device_id=DEVICE_ID)
        # Act
        await status.refresh()
        # Assert
        assert len(status.attributes) == 9

    @staticmethod
    def test_switch():
        """Tests the switch property."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act
        status.switch = True
        # Assert
        assert status.switch

    @staticmethod
    def test_level():
        """Tests the level property."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act
        status.level = 50
        # Assert
        assert status.level == 50

    @staticmethod
    def test_level_range():
        """Tests the level property's range."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        values = [-1, 101]
        for value in values:
            with pytest.raises(ValueError):
                status.level = value

    @staticmethod
    def test_fan_speed():
        """Tests the fan_speed property."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act
        status.fan_speed = 50
        # Assert
        assert status.fan_speed == 50

    @staticmethod
    def test_fan_speed_range():
        """Tests the fan_speed property's range."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        with pytest.raises(ValueError):
            status.level = -1

    @staticmethod
    def test_hue_range():
        """Tests the hue property's range."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        values = [-1, 101]
        for value in values:
            with pytest.raises(ValueError):
                status.hue = value

    @staticmethod
    def test_saturation_range():
        """Tests the hue property's range."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        values = [-1, 101]
        for value in values:
            with pytest.raises(ValueError):
                status.saturation = value

    @staticmethod
    def test_color_temperature_range():
        """Tests the hue property's range."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        values = [0, 30001]
        for value in values:
            with pytest.raises(ValueError):
                status.color_temperature = value

    @staticmethod
    def test_color_format():
        """Tests the color property's validation."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # Act/Assert
        values = ['000000', '#00000', '#HH2000']
        for value in values:
            with pytest.raises(ValueError):
                status.color = value

    @staticmethod
    def test_is_on():
        """Tests the is_on method."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        status.attributes[Attribute.acceleration] = 'active'
        status.attributes[Attribute.level] = 100
        # Act/Assert
        assert status.is_on(Attribute.acceleration)
        assert status.is_on(Attribute.level)
        assert not status.is_on(Attribute.switch)
