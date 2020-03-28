"""Tests for the Device file."""

from pysmartthings.capability import Attribute, Capability
from pysmartthings.device import (
    DEVICE_TYPE_DTH,
    DEVICE_TYPE_UNKNOWN,
    Device,
    DeviceEntity,
    DeviceStatus,
    Status,
)
import pytest

from .conftest import DEVICE_ID, LOCATION_ID, ROOM_ID
from .utilities import get_json


class TestDevice:
    """Tests for the Device class."""

    @staticmethod
    def test_init():
        """Tests whether the Device class initializes correctly."""
        # Arrange/Act
        device = Device()
        # Assert
        assert device.type == DEVICE_TYPE_UNKNOWN
        assert device.capabilities == []
        assert device.components == {}

    @staticmethod
    def test_apply_data():
        """Tests the apply data method."""
        # Arrange
        data = get_json("device.json")
        device = Device()
        # Act
        device.apply_data(data)
        # Assert
        assert device.device_id == DEVICE_ID
        assert device.name == "GE In-Wall Smart Dimmer"
        assert device.label == "Front Porch Lights"
        assert device.location_id == LOCATION_ID
        assert device.room_id == ROOM_ID
        assert device.type == DEVICE_TYPE_DTH
        assert device.device_type_id == "8a9d4b1e3b9b1fe3013b9b206a7f000d"
        assert device.device_type_name == "Dimmer Switch"
        assert device.device_type_network == "ZWAVE"
        assert device.capabilities == [
            "switch",
            "switchLevel",
            "refresh",
            "indicator",
            "sensor",
            "actuator",
            "healthCheck",
            "light",
        ]
        assert device.components == {
            "bottomButton": ["button"],
            "topButton": ["button"],
        }

    @staticmethod
    def test_get_capability():
        """Test the capability retrieval method."""
        # Arrange
        data = get_json("device.json")
        device = Device()
        # Act
        device.apply_data(data)
        # Assert
        assert device.get_capability("switch", "light") == "switch"
        assert device.get_capability("foo", "switch") == "switch"
        assert device.get_capability("foo", "bar") is None


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
        assert device.label == "Front Porch Lights"

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
    async def test_lock(api):
        """Tests the lock method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.lock()
        # Assert
        assert result
        assert not device.status.lock

    @staticmethod
    @pytest.mark.asyncio
    async def test_lock_update(api):
        """Tests the lock method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.lock(True)
        # Assert
        assert result
        assert device.status.lock == "locked"

    @staticmethod
    @pytest.mark.asyncio
    async def test_unlock(api):
        """Tests the unlock method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.unlock()
        # Assert
        assert result
        assert not device.status.lock

    @staticmethod
    @pytest.mark.asyncio
    async def test_unlock_update(api):
        """Tests the unlock method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.unlock(True)
        # Assert
        assert result
        assert device.status.lock == "unlocked"

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
        assert device.status.color == "#4B6432"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_color_hex(api):
        """Tests the set_color method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act
        result = await device.set_color(color_hex="#4B6432")
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
        values = ["000000", "#00000", "#G00000"]
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
        result = await device.set_color(color_hex="#4B6432", set_status=True)
        # Assert
        assert result
        assert device.status.hue == 25
        assert device.status.saturation == 50
        assert device.status.color == "#4B6432"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_fan_mode_legacy(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat)
        device.status.thermostat_fan_mode = "on"
        # Act
        result = await device.set_thermostat_fan_mode("auto")
        # Assert
        assert result
        assert device.status.thermostat_fan_mode != "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_fan_mode(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_fan_mode)
        device.status.thermostat_fan_mode = "on"
        # Act
        result = await device.set_thermostat_fan_mode("auto")
        # Assert
        assert result
        assert device.status.thermostat_fan_mode != "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_fan_mode_update(api):
        """Tests the set_saturation method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_fan_mode)
        device.status.thermostat_fan_mode = "on"
        # Act
        result = await device.set_thermostat_fan_mode("auto", set_status=True)
        # Assert
        assert result
        assert device.status.thermostat_fan_mode == "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_mode_legacy(api):
        """Tests the set_thermostat_mode method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat)
        device.status.thermostat_mode = "heat"
        # Act
        result = await device.set_thermostat_mode("auto")
        # Assert
        assert result
        assert device.status.thermostat_mode != "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_mode(api):
        """Tests the set_thermostat_mode method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_mode)
        device.status.thermostat_mode = "heat"
        # Act
        result = await device.set_thermostat_mode("auto")
        # Assert
        assert result
        assert device.status.thermostat_mode != "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_thermostat_mode_update(api):
        """Tests the set_thermostat_mode method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_mode)
        device.status.thermostat_mode = "heat"
        # Act
        result = await device.set_thermostat_mode("auto", set_status=True)
        # Assert
        assert result
        assert device.status.thermostat_mode == "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_cooling_setpoint_legacy(api):
        """Tests the set_cooling_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat)
        device.status.cooling_setpoint = 70
        # Act
        result = await device.set_cooling_setpoint(76)
        # Assert
        assert result
        assert device.status.cooling_setpoint != 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_cooling_setpoint_mode(api):
        """Tests the set_cooling_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_cooling_setpoint)
        device.status.cooling_setpoint = 70
        # Act
        result = await device.set_cooling_setpoint(76)
        # Assert
        assert result
        assert device.status.cooling_setpoint != 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_cooling_setpoint_update(api):
        """Tests the set_cooling_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_cooling_setpoint)
        device.status.cooling_setpoint = 70
        # Act
        result = await device.set_cooling_setpoint(76, set_status=True)
        # Assert
        assert result
        assert device.status.cooling_setpoint == 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_heating_setpoint_legacy(api):
        """Tests the set_heating_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat)
        device.status.heating_setpoint = 70
        # Act
        result = await device.set_heating_setpoint(76)
        # Assert
        assert result
        assert device.status.heating_setpoint != 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_heating_setpoint_mode(api):
        """Tests the set_heating_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_heating_setpoint)
        device.status.heating_setpoint = 70
        # Act
        result = await device.set_heating_setpoint(76)
        # Assert
        assert result
        assert device.status.heating_setpoint != 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_heating_setpoint_update(api):
        """Tests the set_heating_setpoint method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.thermostat_heating_setpoint)
        device.status.heating_setpoint = 70
        # Act
        result = await device.set_heating_setpoint(76, set_status=True)
        # Assert
        assert result
        assert device.status.heating_setpoint == 76

    @staticmethod
    @pytest.mark.asyncio
    async def test_open(api):
        """Tests the open method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.door_control)
        # Act/Assert
        assert await device.open()
        assert device.status.door is None
        assert await device.open(set_status=True)
        assert device.status.door == "opening"

    @staticmethod
    @pytest.mark.asyncio
    async def test_open_legacy(api):
        """Tests the open method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.garage_door_control)
        # Act/Assert
        assert await device.open()
        assert device.status.door is None
        assert await device.open(set_status=True)
        assert device.status.door == "opening"

    @staticmethod
    @pytest.mark.asyncio
    async def test_close(api):
        """Tests the close method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.door_control)
        # Act/Assert
        assert await device.close()
        assert device.status.door is None
        assert await device.close(set_status=True)
        assert device.status.door == "closing"

    @staticmethod
    @pytest.mark.asyncio
    async def test_close_legacy(api):
        """Tests the close method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.garage_door_control)
        # Act/Assert
        assert await device.close()
        assert device.status.door is None
        assert await device.close(set_status=True)
        assert device.status.door == "closing"

    @staticmethod
    @pytest.mark.asyncio
    async def test_open_window_shade(api):
        """Tests the open method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.window_shade)
        # Act/Assert
        assert await device.open()
        assert device.status.window_shade is None
        assert await device.open(set_status=True)
        assert device.status.window_shade == "opening"

    @staticmethod
    @pytest.mark.asyncio
    async def test_close_window_shade(api):
        """Tests the close method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        device.capabilities.append(Capability.window_shade)
        # Act/Assert
        assert await device.close()
        assert device.status.window_shade is None
        assert await device.close(set_status=True)
        assert device.status.window_shade == "closing"

    @staticmethod
    @pytest.mark.asyncio
    async def test_request_drlc_action(api):
        """Tests the request_drlc_action method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.request_drlc_action(1, 2, "1970-01-01T00:00:00Z", 10, 1)
        assert device.status.drlc_status is None
        assert await device.request_drlc_action(
            1, 2, "1970-01-01T00:00:00Z", 10, 1, set_status=True
        )
        assert device.status.drlc_status == {
            "duration": 10,
            "drlcLevel": 2,
            "start": "1970-01-01T00:00:00Z",
            "override": False,
        }

    @staticmethod
    @pytest.mark.asyncio
    async def test_override_drlc_action(api):
        """Tests the override_drlc_action method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.override_drlc_action(True)
        assert device.status.drlc_status is None
        assert await device.override_drlc_action(True, set_status=True)
        assert device.status.drlc_status == {"override": True}

    @staticmethod
    @pytest.mark.asyncio
    async def test_execute(api):
        """Tests the execute method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.execute("Test", {"data": "Test"})

    @staticmethod
    @pytest.mark.asyncio
    async def test_preset_position(api):
        """Tests the preset_position method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.preset_position()

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_air_conditioner_mode(api):
        """Tests the set_air_conditioner_mode method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.set_air_conditioner_mode("auto")
        assert device.status.air_conditioner_mode is None
        assert await device.set_air_conditioner_mode("auto", set_status=True)
        assert device.status.air_conditioner_mode == "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_fan_mode(api):
        """Tests the set_fan_mode method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.set_fan_mode("auto")
        assert device.status.fan_mode is None
        assert await device.set_fan_mode("auto", set_status=True)
        assert device.status.fan_mode == "auto"

    @staticmethod
    @pytest.mark.asyncio
    async def test_set_air_flow_direction(api):
        """Tests the set_air_flow_direction method."""
        # Arrange
        device = DeviceEntity(api, device_id=DEVICE_ID)
        # Act/Assert
        assert await device.set_air_flow_direction("fixed")
        assert device.status.air_flow_direction is None
        assert await device.set_air_flow_direction("fixed", set_status=True)
        assert device.status.air_flow_direction == "fixed"


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
        assert status.component_id == "main"

    @staticmethod
    def test_apply_data():
        """Tests the apply_data method."""
        # Arrange
        data = get_json("device_status.json")
        # Act
        status = DeviceStatus(None, DEVICE_ID, data)
        # Assert
        assert len(status.attributes) == 9
        assert status.switch
        assert status.level == 100
        assert len(status.components) == 2
        assert len(status.components["topButton"].attributes) == 3
        assert len(status.components["bottomButton"].attributes) == 3

    @staticmethod
    def test_apply_attribute_update():
        """Tests the apply_attribute_update method."""
        # Arrange
        data = get_json("device_status.json")
        device = DeviceStatus(None, DEVICE_ID, data)
        # Act
        device.apply_attribute_update(
            "main", Capability.switch_level, Attribute.level, 50, "%", {"test": "test"}
        )
        # Assert
        status = device.attributes[Attribute.level]
        assert status.value == 50
        assert status.unit == "%"
        assert status.data == {"test": "test"}

    @staticmethod
    def test_apply_attribute_update_preserve_unit():
        """Tests the apply_attribute_update preserves the old unit."""
        # Arrange
        data = get_json("device_status.json")
        device = DeviceStatus(None, DEVICE_ID, data)
        device.attributes[Capability.switch_level] = Status(40, "%", None)
        # Act
        device.apply_attribute_update(
            "main", Capability.switch_level, Attribute.level, 50
        )
        # Assert
        status = device.attributes[Attribute.level]
        assert status.unit == "%"

    @staticmethod
    def test_apply_attribute_update_child_status():
        """Tests the apply_attribute_update method to a child status."""
        # Arrange
        data = get_json("device_status.json")
        status = DeviceStatus(None, DEVICE_ID, data)
        # Act
        status.apply_attribute_update("bottomButton", "switchLevel", "level", 50)
        # Assert
        assert status.components["bottomButton"].level == 50

    @staticmethod
    def test_values():
        """Test the values property."""
        # Arrange
        data = get_json("device_status.json")
        status = DeviceStatus(None, DEVICE_ID, data)
        # Act/Assert
        assert status.values == {
            "button": None,
            "numberOfButtons": None,
            "supportedButtonValues": None,
            "indicatorStatus": "when off",
            "switch": "on",
            "checkInterval": 1920,
            "healthStatus": None,
            "DeviceWatch-DeviceStatus": None,
            "level": 100,
        }

    @staticmethod
    def test_attributes():
        """Test the attributes property."""
        # Arrange
        data = get_json("device_status.json")
        status = DeviceStatus(None, DEVICE_ID, data)
        # Act/Assert
        assert status.attributes == {
            "button": (None, None, None),
            "numberOfButtons": (None, None, None),
            "supportedButtonValues": (None, None, None),
            "indicatorStatus": ("when off", None, None),
            "switch": ("on", None, None),
            "checkInterval": (
                1920,
                "s",
                {"protocol": "zwave", "hubHardwareId": "000F"},
            ),
            "healthStatus": (None, None, {}),
            "DeviceWatch-DeviceStatus": (None, None, {}),
            "level": (100, "%", None),
        }

    @staticmethod
    def test_attributes_default():
        """Test the attributes property."""
        # Arrange
        data = get_json("device_status.json")
        status = DeviceStatus(None, DEVICE_ID, data)
        # Act/Assert
        assert status.attributes["thermostatSetpoint"] == (None, None, None)

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
            status.fan_speed = -1

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
        values = ["000000", "#00000", "#HH2000"]
        for value in values:
            with pytest.raises(ValueError):
                status.color = value

    @staticmethod
    def test_is_on():
        """Tests the is_on method."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)
        status.update_attribute_value(Attribute.acceleration, "active")
        status.level = 100
        # Act/Assert
        assert status.is_on(Attribute.acceleration)
        assert status.is_on(Attribute.level)
        assert not status.is_on(Attribute.switch)

    @staticmethod
    def test_well_known_attributes():
        """Tests the humidity property."""
        # Arrange
        status = DeviceStatus(None, device_id=DEVICE_ID)

        assert status.supported_ac_modes == []
        assert status.supported_ac_fan_modes == []

        status.update_attribute_value(Attribute.humidity, 50)
        status.update_attribute_value(Attribute.temperature, 55)
        status.update_attribute_value(Attribute.thermostat_operating_state, "on")
        status.update_attribute_value(
            Attribute.supported_thermostat_fan_modes, ["on", "off"]
        )
        status.update_attribute_value(
            Attribute.supported_thermostat_modes, ["auto", "off"]
        )
        status.update_attribute_value(Attribute.lock, "locked")
        status.update_attribute_value(Attribute.door, "open")
        status.update_attribute_value(Attribute.window_shade, "closed")
        status.update_attribute_value(Attribute.data, {"test": "test"})
        status.update_attribute_value(Attribute.three_axis, [0, 0, 0])
        status.update_attribute_value(Attribute.supported_ac_modes, ["auto", "cool"])
        status.update_attribute_value(Attribute.fan_mode, "low")
        status.update_attribute_value(Attribute.supported_ac_fan_modes, ["auto", "low"])
        # Act/Assert
        assert status.humidity == 50
        assert status.temperature == 55
        assert status.thermostat_operating_state == "on"
        assert status.supported_thermostat_fan_modes == ["on", "off"]
        assert status.supported_thermostat_modes == ["auto", "off"]
        assert status.lock == "locked"
        assert status.door == "open"
        assert status.window_shade == "closed"
        assert status.data == {"test": "test"}
        assert status.three_axis == [0, 0, 0]
        assert status.supported_ac_modes == ["auto", "cool"]
        assert status.supported_ac_fan_modes == ["auto", "low"]

    @staticmethod
    def test_well_known_ocf_attributes():
        """Tests the OCF related attributes."""
        # Arrange
        data = get_json("device_samsungac_status.json")
        status = DeviceStatus(None, device_id=DEVICE_ID, data=data)
        # Act/Assert
        assert status.ocf_data_model_version == "res.1.1.0,sh.1.1.0"
        assert status.ocf_date_of_manufacture == "2019-02-26T02:05:55Z"
        assert status.ocf_device_id == DEVICE_ID
        assert status.ocf_firmware_version == "0.1.0"
        assert status.ocf_hardware_version == "1.0"
        assert status.ocf_manufacturer_details_link == "http://www.samsung.com"
        assert status.ocf_manufacturer_name == "Samsung Electronics"
        assert (
            status.ocf_model_number
            == "ARTIK051_KRAC_18K|10193441|60010123001111010200000000000000"
        )
        assert status.ocf_name == "Air Conditioner"
        assert status.ocf_os_version == "TizenRT2.0"
        assert status.ocf_platform_id == "d5226d90-1b4f-e59d-5f3f-027ac3b18faf"
        assert status.ocf_platform_version == "0.1.0"
        assert status.ocf_spec_version == "core.1.1.0"
        assert status.ocf_support_link == "http://www.samsung.com/support"
        assert status.ocf_system_time == "02:05:55Z"
        assert status.ocf_vendor_id == "DA-AC-RAC-000001"

    @staticmethod
    def test_well_known_drlc_attributes():
        """Tests the drlc related attributes."""
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # No attribute
        assert status.drlc_status is None
        assert status.drlc_status_duration is None
        assert status.drlc_status_level is None
        assert status.drlc_status_override is None
        assert status.drlc_status_start is None
        # Populated
        drlc_status = {
            "duration": 0,
            "drlcLevel": -1,
            "start": "1970-01-01T00:00:00Z",
            "override": False,
        }
        status.update_attribute_value(Attribute.drlc_status, drlc_status)
        assert status.drlc_status == drlc_status
        assert status.drlc_status_duration == 0
        assert status.drlc_status_level == -1
        assert not status.drlc_status_override
        assert status.drlc_status_start == "1970-01-01T00:00:00Z"
        # Missing
        status.update_attribute_value(Attribute.drlc_status, {})
        assert status.drlc_status == {}
        assert status.drlc_status_duration is None
        assert status.drlc_status_level is None
        assert status.drlc_status_override is None
        assert status.drlc_status_start is None
        # Not valid
        drlc_status = {"duration": "Foo", "drlcLevel": "Foo"}
        status.update_attribute_value(Attribute.drlc_status, drlc_status)
        assert status.drlc_status == drlc_status
        assert status.drlc_status_duration is None
        assert status.drlc_status_level is None

    @staticmethod
    def test_well_known_power_consumption_attributes():
        """Tests the power consumption related attributes."""
        status = DeviceStatus(None, device_id=DEVICE_ID)
        # No attribute
        assert status.power_consumption is None
        assert status.power_consumption_end is None
        assert status.power_consumption_energy is None
        assert status.power_consumption_power is None
        assert status.power_consumption_start is None
        # Populated
        data = {
            "start": "2019-02-24T21:03:04Z",
            "power": 0,
            "energy": 500,
            "end": "2019-02-26T02:05:55Z",
        }
        status.update_attribute_value(Attribute.power_consumption, data)
        assert status.power_consumption == data
        assert status.power_consumption_end == "2019-02-26T02:05:55Z"
        assert status.power_consumption_energy == 500
        assert status.power_consumption_power == 0
        assert status.power_consumption_start == "2019-02-24T21:03:04Z"
        # Missing
        status.update_attribute_value(Attribute.power_consumption, {})
        assert status.power_consumption == {}
        assert status.power_consumption_end is None
        assert status.power_consumption_energy is None
        assert status.power_consumption_power is None
        assert status.power_consumption_start is None
        # Not valid
        data = {"power": "Foo", "energy": "Bar"}
        status.update_attribute_value(Attribute.power_consumption, data)
        assert status.power_consumption == data
        assert status.power_consumption_energy is None
        assert status.power_consumption_power is None
