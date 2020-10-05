"""Defines a SmartThings device."""
from collections import defaultdict, namedtuple
import colorsys
import re
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from .api import Api
from .capability import ATTRIBUTE_OFF_VALUES, ATTRIBUTE_ON_VALUES, Attribute, Capability
from .entity import Entity

DEVICE_TYPE_OCF = "OCF"
DEVICE_TYPE_DTH = "DTH"
DEVICE_TYPE_UNKNOWN = "UNKNOWN"
DEVICE_TYPE_ENDPOINT_APP = "ENDPOINT_APP"
DEVICE_TYPE_VIPER = "VIPER"

COLOR_HEX_MATCHER = re.compile("^#[A-Fa-f0-9]{6}$")
Status = namedtuple("status", "value unit data")
STATUS_NONE = Status(None, None, None)


def hs_to_hex(hue: float, saturation: float) -> str:
    """Convert hue and saturation to a string hex color."""
    rgb = colorsys.hsv_to_rgb(hue / 100, saturation / 100, 100)
    return "#{:02x}{:02x}{:02x}".format(
        round(rgb[0]), round(rgb[1]), round(rgb[2])
    ).upper()


def hex_to_hs(color_hex: str) -> (int, int):
    """Convert a string hex color to hue and saturation components."""
    color_hex = color_hex.lstrip("#")
    rgb = [
        int(color_hex[i : i + len(color_hex) // 3], 16) / 255.0
        for i in range(0, len(color_hex), len(color_hex) // 3)
    ]
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    return round(hsv[0] * 100, 3), round(hsv[1] * 100, 3)


def bool_to_value(attribute: str, value: bool) -> str:
    """Convert bool value to ON/OFF value of given attribute."""
    return ATTRIBUTE_ON_VALUES[attribute] if value else ATTRIBUTE_OFF_VALUES[attribute]


class Command:
    """Define common commands."""

    close = "close"
    execute = "execute"
    lock = "lock"
    off = "off"
    open = "open"
    on = "on"
    override_drlc_action = "overrideDrlcAction"
    preset_position = "presetPosition"
    request_drlc_action = "requestDrlcAction"
    set_air_flow_direction = "setAirFlowDirection"
    set_air_conditioner_mode = "setAirConditionerMode"
    set_color = "setColor"
    set_color_temperature = "setColorTemperature"
    set_cooling_setpoint = "setCoolingSetpoint"
    set_fan_mode = "setFanMode"
    set_fan_speed = "setFanSpeed"
    set_heating_setpoint = "setHeatingSetpoint"
    set_hue = "setHue"
    set_level = "setLevel"
    set_saturation = "setSaturation"
    set_thermostat_fan_mode = "setThermostatFanMode"
    set_thermostat_mode = "setThermostatMode"
    unlock = "unlock"
    mute = "mute"
    unmute = "unmute"
    set_volume = "setVolume"
    volume_up = "volumeUp"
    volume_down = "volumeDown"
    play = "play"
    pause = "pause"
    stop = "stop"
    fast_forward = "fastForward"
    rewind = "rewind"
    set_input_source = "setInputSource"
    set_playback_shuffle = "setPlaybackShuffle"
    set_playback_repeat_mode = "setPlaybackRepeatMode"
    set_tv_channel = "setTvChannel"
    channel_up = "channelUp"
    channel_down = "channelDown"


class Device:
    """Represents a SmartThings device."""

    def __init__(self):
        """Initialize a new device."""
        self._device_id = None
        self._name = None
        self._label = None
        self._location_id = None
        self._room_id = None
        self._type = DEVICE_TYPE_UNKNOWN
        self._device_type_id = None
        self._device_type_name = None
        self._device_type_network = None
        self._components = dict()
        self._capabilities = []

    def apply_data(self, data: dict):
        """Apply the given data dictionary."""
        self._device_id = data.get("deviceId")
        self._name = data.get("name")
        self._label = data.get("label")
        self._location_id = data.get("locationId")
        self._room_id = data.get("roomId")
        self._type = data.get("type")
        self._components.clear()
        self._capabilities.clear()

        components = data.get("components")
        if components:
            for component in components:
                capabilities = [c["id"] for c in component["capabilities"]]
                component_id = component["id"]
                if component_id == "main":
                    self._capabilities.extend(capabilities)
                else:
                    self._components[component_id] = capabilities

        if self._type == DEVICE_TYPE_DTH:
            dth = data.get("dth")
            if dth:
                self._device_type_id = dth.get("deviceTypeId")
                self._device_type_name = dth.get("deviceTypeName")
                self._device_type_network = dth.get("deviceNetworkType")

    def get_capability(self, *capabilities) -> Optional[str]:
        """Return the first capability held by the device."""
        for capability in capabilities:
            if capability in self._capabilities:
                return capability
        return None

    @property
    def device_id(self) -> str:
        """Get the SmartThings device id."""
        return self._device_id

    @property
    def name(self) -> str:
        """Get the SmartThings device name."""
        return self._name

    @property
    def label(self) -> str:
        """Get the SmartThings user assigned label."""
        return self._label

    @property
    def location_id(self) -> str:
        """Get the SmartThings location assigned to the device."""
        return self._location_id

    @property
    def room_id(self):
        """Get the room assigned to the device."""
        return self._room_id

    @property
    def type(self) -> str:
        """Get the SmartThings device type."""
        return self._type

    @property
    def device_type_id(self) -> str:
        """Get the SmartThings device type handler id."""
        return self._device_type_id

    @property
    def device_type_name(self) -> str:
        """Get the SmartThings device type handler name."""
        return self._device_type_name

    @property
    def device_type_network(self) -> str:
        """Get the SmartThings device type handler network."""
        return self._device_type_network

    @property
    def components(self) -> Dict[str, Sequence[str]]:
        """Get the components of the device."""
        return self._components

    @property
    def capabilities(self) -> Sequence[str]:
        """Get a unique list of all capabilities across components."""
        return self._capabilities


class DeviceStatusBase:
    """Define the base status of device components."""

    def __init__(
        self, component_id: str, attributes: Optional[Mapping[str, Status]] = None
    ):
        """Initialize the status class."""
        self._attributes = defaultdict(lambda: STATUS_NONE, attributes or {})
        self._component_id = component_id

    def is_on(self, attribute: str) -> bool:
        """Determine if a specific attribute contains an on/True value."""
        if attribute not in ATTRIBUTE_ON_VALUES:
            return bool(self._attributes[attribute].value)
        return self._attributes[attribute].value == ATTRIBUTE_ON_VALUES[attribute]

    def update_attribute_value(self, attribute: str, value):
        """Update the value of an attribute while maintaining unit and data."""
        status = self._attributes[attribute]
        self._attributes[attribute] = Status(value, status.unit, status.data)

    @property
    def attributes(self) -> Dict[str, Status]:
        """Get all of the attribute status objects."""
        return self._attributes

    @property
    def values(self) -> Dict[str, Any]:
        """Get the values of the attributes."""
        return defaultdict(
            lambda: None, {k: v.value for k, v in self._attributes.items()}
        )

    @property
    def color(self) -> Optional[str]:
        """Get the color attribute."""
        return self._attributes[Attribute.color].value

    @color.setter
    def color(self, value: str):
        """Set the color attribute."""
        if not COLOR_HEX_MATCHER.match(value):
            raise ValueError(
                "value was not a properly formatted color hex, i.e. #000000."
            )
        self.update_attribute_value(Attribute.color, value)

    @property
    def color_temperature(self) -> int:
        """Get the color temperature attribute."""
        return int(self._attributes[Attribute.color_temperature].value or 1)

    @color_temperature.setter
    def color_temperature(self, value: int):
        """Set the color temperature attribute."""
        if not 1 <= value <= 30000:
            raise ValueError("value must be scaled between 1-30000.")
        self.update_attribute_value(Attribute.color_temperature, value)

    @property
    def component_id(self) -> str:
        """Get the component id of the status."""
        return self._component_id

    @property
    def fan_speed(self) -> int:
        """Get the fan speed attribute."""
        return int(self._attributes[Attribute.fan_speed].value or 0)

    @fan_speed.setter
    def fan_speed(self, value: int):
        """Set the fan speed attribute."""
        if value < 0:
            raise ValueError("value must be >= 0.")
        self.update_attribute_value(Attribute.fan_speed, value)

    @property
    def hue(self) -> float:
        """Get the hue attribute, scaled 0-100."""
        return float(self._attributes[Attribute.hue].value or 0.0)

    @hue.setter
    def hue(self, value: float):
        """Set the hue attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self.update_attribute_value(Attribute.hue, value)

    @property
    def level(self) -> int:
        """Get the level attribute, scaled 0-100."""
        return int(self._attributes[Attribute.level].value or 0)

    @level.setter
    def level(self, value: int):
        """Set the level of the attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self.update_attribute_value(Attribute.level, value)

    @property
    def saturation(self) -> float:
        """Get the saturation attribute, scaled 0-100."""
        return float(self._attributes[Attribute.saturation].value or 0.0)

    @saturation.setter
    def saturation(self, value: float):
        """Set the saturation attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self.update_attribute_value(Attribute.saturation, value)

    @property
    def motion(self) -> bool:
        """Get the motion attribute."""
        return self.is_on(Attribute.motion)

    @property
    def switch(self) -> bool:
        """Get the switch attribute."""
        return self.is_on(Attribute.switch)

    @switch.setter
    def switch(self, value: bool):
        """Set the value of the switch attribute."""
        status_value = bool_to_value(Attribute.switch, value)
        self.update_attribute_value(Attribute.switch, status_value)

    @property
    def thermostat_fan_mode(self):
        """Get the thermostatFanMode attribute."""
        return self._attributes[Attribute.thermostat_fan_mode].value

    @thermostat_fan_mode.setter
    def thermostat_fan_mode(self, value: str):
        """Update the thermostatFanMode attribute."""
        self.update_attribute_value(Attribute.thermostat_fan_mode, value)

    @property
    def humidity(self) -> Optional[int]:
        """Get the humidity in percentage."""
        return self._attributes[Attribute.humidity].value

    @property
    def thermostat_mode(self) -> Optional[str]:
        """Get the thermostatMode attribute."""
        return self._attributes[Attribute.thermostat_mode].value

    @thermostat_mode.setter
    def thermostat_mode(self, value: str):
        """Set the thermostatMode attribute."""
        self.update_attribute_value(Attribute.thermostat_mode, value)

    @property
    def temperature(self) -> Optional[int]:
        """Get the temperature attribute."""
        return self._attributes[Attribute.temperature].value

    @property
    def thermostat_operating_state(self) -> Optional[str]:
        """Get the thermostatOperatingState attribute."""
        return self._attributes[Attribute.thermostat_operating_state].value

    @property
    def supported_thermostat_fan_modes(self) -> Optional[str]:
        """Get the supportedThermostatFanModes attribute."""
        return self._attributes[Attribute.supported_thermostat_fan_modes].value

    @property
    def supported_thermostat_modes(self) -> Optional[str]:
        """Get the supportedThermostatModes attribute."""
        return self._attributes[Attribute.supported_thermostat_modes].value

    @property
    def cooling_setpoint(self) -> Optional[int]:
        """Get the coolingSetpoint attribute."""
        return self._attributes[Attribute.cooling_setpoint].value

    @cooling_setpoint.setter
    def cooling_setpoint(self, value: int):
        """Set the coolingSetpoint attribute."""
        self.update_attribute_value(Attribute.cooling_setpoint, value)

    @property
    def heating_setpoint(self) -> Optional[int]:
        """Get the heatingSetpoint attribute."""
        return self._attributes[Attribute.heating_setpoint].value

    @heating_setpoint.setter
    def heating_setpoint(self, value):
        """Set the heatingSetpoint attribute."""
        self.update_attribute_value(Attribute.heating_setpoint, value)

    @property
    def lock(self):
        """Get the lock attribute."""
        return self._attributes[Attribute.lock].value

    @property
    def door(self):
        """Get the door attribute."""
        return self._attributes[Attribute.door].value

    @property
    def window_shade(self):
        """Get the windowShade attribute."""
        return self._attributes[Attribute.window_shade].value

    @property
    def drlc_status(self) -> Optional[dict]:
        """Get the demand response load control status."""
        return self._attributes[Attribute.drlc_status].value

    @property
    def drlc_status_duration(self) -> Optional[int]:
        """Get the duration component of the drlc status."""
        try:
            return int(self.drlc_status["duration"])
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def drlc_status_level(self) -> Optional[int]:
        """Get the level component of the drlc status."""
        try:
            return int(self.drlc_status["drlcLevel"])
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def drlc_status_start(self) -> Optional[str]:
        """Get the level component of the drlc status."""
        try:
            return self.drlc_status["start"]
        except (KeyError, TypeError):
            return None

    @property
    def drlc_status_override(self) -> Optional[bool]:
        """Get the override component of the drlc status."""
        try:
            return bool(self.drlc_status["override"])
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def power_consumption(self) -> Optional[dict]:
        """Get the power consumption report data."""
        return self._attributes[Attribute.power_consumption].value

    @property
    def power_consumption_start(self) -> Optional[str]:
        """Get the start component of power consumption data."""
        try:
            return self.power_consumption["start"]
        except (KeyError, TypeError):
            return None

    @property
    def power_consumption_power(self) -> Optional[int]:
        """Get the power component of power consumption data."""
        try:
            return int(self.power_consumption["power"])
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def power_consumption_energy(self) -> Optional[int]:
        """Get the energy component of power consumption data."""
        try:
            return int(self.power_consumption["energy"])
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def power_consumption_end(self) -> Optional[str]:
        """Get the end component of power consumption data."""
        try:
            return self.power_consumption["end"]
        except (KeyError, TypeError):
            return None

    @property
    def ocf_system_time(self) -> Optional[str]:
        """Get the OCF system time."""
        return self._attributes[Attribute.st].value

    @property
    def ocf_firmware_version(self) -> Optional[str]:
        """Get the OCF firmware version."""
        return self._attributes[Attribute.mnfv].value

    @property
    def ocf_date_of_manufacture(self) -> Optional[str]:
        """Get the OCF date of manufacture."""
        return self._attributes[Attribute.mndt].value

    @property
    def ocf_hardware_version(self) -> Optional[str]:
        """Get the OCF hardware version."""
        return self._attributes[Attribute.mnhw].value

    @property
    def ocf_device_id(self) -> Optional[str]:
        """Get the OCF device id."""
        return self._attributes[Attribute.di].value

    @property
    def ocf_support_link(self) -> Optional[str]:
        """Get the OCF support link."""
        return self._attributes[Attribute.mnsl].value

    @property
    def ocf_data_model_version(self) -> Optional[str]:
        """Get the OCF data model version."""
        return self._attributes[Attribute.dmv].value

    @property
    def ocf_name(self) -> Optional[str]:
        """Get the OCF name."""
        return self._attributes[Attribute.n].value

    @property
    def ocf_vendor_id(self) -> Optional[str]:
        """Get the OCF vendor id."""
        return self._attributes[Attribute.vid].value

    @property
    def ocf_model_number(self):
        """Get the OCF model number."""
        return self._attributes[Attribute.mnmo].value

    @property
    def ocf_manufacturer_name(self) -> Optional[str]:
        """Get the OCF manufacturer name."""
        return self._attributes[Attribute.mnmn].value

    @property
    def ocf_manufacturer_details_link(self) -> Optional[str]:
        """Get the OCF manufacturer details link."""
        return self._attributes[Attribute.mnml].value

    @property
    def ocf_platform_version(self) -> Optional[str]:
        """Get the OCF platform version."""
        return self._attributes[Attribute.mnpv].value

    @property
    def ocf_os_version(self) -> Optional[str]:
        """Get the OCF OS version."""
        return self._attributes[Attribute.mnos].value

    @property
    def ocf_platform_id(self) -> Optional[str]:
        """Get the OCF platform id."""
        return self._attributes[Attribute.pi].value

    @property
    def ocf_spec_version(self) -> Optional[str]:
        """Get the OCF spec version."""
        return self._attributes[Attribute.icv].value

    @property
    def data(self) -> Optional[dict]:
        """Get the data attribute."""
        return self._attributes[Attribute.data].value

    @property
    def air_conditioner_mode(self) -> Optional[str]:
        """Get the air conditioner mode attribute."""
        return self._attributes[Attribute.air_conditioner_mode].value

    @property
    def supported_ac_modes(self) -> Sequence[str]:
        """Get the supported AC modes attribute."""
        value = self._attributes[Attribute.supported_ac_modes].value
        # pylint: disable=isinstance-second-argument-not-valid-type
        if isinstance(value, Sequence):
            return sorted(value)
        return []

    @property
    def fan_mode(self) -> Optional[str]:
        """Get the fan mode attribute."""
        return self._attributes[Attribute.fan_mode].value

    @property
    def supported_ac_fan_modes(self) -> Sequence[str]:
        """Get the supported AC fan modes attribute."""
        value = self._attributes[Attribute.supported_ac_fan_modes].value
        # pylint: disable=isinstance-second-argument-not-valid-type
        if isinstance(value, Sequence):
            return sorted(value)
        return []

    @property
    def air_flow_direction(self) -> str:
        """Get the airFlowDirection attribute."""
        return self._attributes[Attribute.air_flow_direction].value

    @property
    def three_axis(self) -> Optional[Tuple[int, int, int]]:
        """Get the three axis attribute."""
        return self._attributes[Attribute.three_axis].value

    @property
    def mute(self) -> bool:
        """Get the mute attribute."""
        return self.is_on(Attribute.mute)

    @mute.setter
    def mute(self, value: bool):
        """Set the mute attribute."""
        status_value = bool_to_value(Attribute.mute, value)
        self.update_attribute_value(Attribute.mute, status_value)

    @property
    def volume(self) -> int:
        """Get the volume attribute."""
        return self._attributes[Attribute.volume].value

    @volume.setter
    def volume(self, value: float):
        """Set the volume attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self.update_attribute_value(Attribute.volume, value)

    @property
    def playback_status(self) -> str:
        """Get the playbackStatus attribute."""
        return self._attributes[Attribute.playback_status].value

    @playback_status.setter
    def playback_status(self, value: str):
        """Set the playbackStatus attribute."""
        self.update_attribute_value(Attribute.playback_status, value)

    @property
    def input_source(self) -> str:
        """Get the inputSource attribute."""
        return self._attributes[Attribute.input_source].value

    @input_source.setter
    def input_source(self, value: str):
        """Set the volume attribute."""
        if value not in self.supported_input_sources:
            raise ValueError("value must be supported.")
        self.update_attribute_value(Attribute.input_source, value)

    @property
    def supported_input_sources(self) -> Sequence[str]:
        """Get the supportedInputSources attribute."""
        value = self._attributes[Attribute.supported_input_sources].value
        if "value" in value:
            return value["value"]
        return value

    @property
    def playback_shuffle(self) -> bool:
        """Get the playbackShuffle attribute."""
        return self.is_on(Attribute.playback_shuffle)

    @playback_shuffle.setter
    def playback_shuffle(self, value: bool):
        """Set the playbackShuffle attribute."""
        status_value = bool_to_value(Attribute.playback_shuffle, value)
        self.update_attribute_value(Attribute.playback_shuffle, status_value)

    @property
    def playback_repeat_mode(self) -> str:
        """Get the playbackRepeatMode attribute."""
        return self._attributes[Attribute.playback_repeat_mode].value

    @playback_repeat_mode.setter
    def playback_repeat_mode(self, value: str):
        """Set the playbackRepeatMode attribute."""
        if value not in ["all", "off", "one"]:
            raise ValueError("value must be one of: all, off, one")
        self.update_attribute_value(Attribute.playback_repeat_mode, value)

    @property
    def tv_channel(self) -> str:
        """Get the tvChannel attribute."""
        return self._attributes[Attribute.tv_channel].value

    @tv_channel.setter
    def tv_channel(self, value: str):
        """Set the tvChannel attribute."""
        self.update_attribute_value(Attribute.tv_channel, value)

    @property
    def media_title(self) -> bool:
        """Get the trackDescription attribute."""
        return self._attributes["trackDescription"].value


class DeviceStatus(DeviceStatusBase):
    """Define the device status."""

    def __init__(self, api: Api, device_id: str, data=None):
        """Create a new instance of the DeviceStatusEntity class."""
        super().__init__("main")
        self._api = api
        self._device_id = device_id
        self._components = {}
        if data:
            self.apply_data(data)

    def apply_attribute_update(
        self,
        component_id: str,
        capability: str,
        attribute: str,
        value: Any,
        unit: Optional[str] = None,
        data: Optional[Dict] = None,
    ):
        """Apply an update to a specific attribute."""
        component = self
        if component_id != "main" and component_id in self._components:
            component = self._components[component_id]

        # preserve unit until fixed in the API
        old_status = component.attributes[attribute]
        component.attributes[attribute] = Status(value, unit or old_status.unit, data)

    def apply_data(self, data: dict):
        """Apply the values from the given data structure."""
        self._components.clear()
        for component_id, component in data["components"].items():
            attributes = {}
            for capabilities in component.values():
                for attribute, value in capabilities.items():
                    attributes[attribute] = Status(
                        value.get("value"), value.get("unit"), value.get("data")
                    )
            if component_id == "main":
                self._attributes.clear()
                self._attributes.update(attributes)
            else:
                self._components[component_id] = DeviceStatusBase(
                    component_id, attributes
                )

    @property
    def components(self) -> Dict[str, DeviceStatusBase]:
        """Get the component status instances."""
        return self._components

    @property
    def device_id(self) -> str:
        """Get the device id."""
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        """Set the device id."""
        self._device_id = value

    async def refresh(self):
        """Refresh the values of the entity."""
        data = await self._api.get_device_status(self.device_id)
        if data:
            self.apply_data(data)


class DeviceEntity(Entity, Device):
    """Define a device entity."""

    def __init__(
        self, api: Api, data: Optional[dict] = None, device_id: Optional[str] = None
    ):
        """Create a new instance of the DeviceEntity class."""
        Entity.__init__(self, api)
        Device.__init__(self)
        if data:
            self.apply_data(data)
        if device_id:
            self._device_id = device_id
        self._status = DeviceStatus(api, self._device_id)

    async def refresh(self):
        """Refresh the device information using the API."""
        data = await self._api.get_device(self._device_id)
        if data:
            self.apply_data(data)
        self._status.device_id = self._device_id

    async def save(self):
        """Save the changes made to the device."""
        raise NotImplementedError

    async def command(self, component_id: str, capability, command, args=None) -> bool:
        """Execute a command on the device."""
        response = await self._api.post_device_command(
            self._device_id, component_id, capability, command, args
        )
        try:
            return response["results"][0]["status"] in ("ACCEPTED", "COMPLETED")
        except (KeyError, IndexError):
            return False

    async def set_color(
        self,
        hue: Optional[float] = None,
        saturation: Optional[float] = None,
        color_hex: Optional[str] = None,
        set_status: bool = False,
        *,
        component_id: str = "main"
    ) -> bool:
        """Call the set color command."""
        color_map = {}
        if color_hex:
            if not COLOR_HEX_MATCHER.match(color_hex):
                raise ValueError(
                    "color_hex was not a properly formatted " "color hex, i.e. #000000."
                )
            color_map["hex"] = color_hex
        else:
            if not 0 <= hue <= 100:
                raise ValueError("hue must be scaled between 0-100.")
            if not 0 <= saturation <= 100:
                raise ValueError("saturation must be scaled between 0-100.")
            color_map["hue"] = hue
            color_map["saturation"] = saturation

        result = await self.command(
            component_id, Capability.color_control, Command.set_color, [color_map]
        )
        if result and set_status:
            if color_hex:
                self.status.color = color_hex
                self.status.hue, self.status.saturation = hex_to_hs(color_hex)
            else:
                self.status.color = hs_to_hex(hue, saturation)
                self.status.hue = hue
                self.status.saturation = saturation
        return result

    async def set_color_temperature(
        self, temperature: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the color temperature device command."""
        if not 1 <= temperature <= 30000:
            raise ValueError("temperature must be scaled between 1-30000.")

        result = await self.command(
            component_id,
            Capability.color_temperature,
            Command.set_color_temperature,
            [temperature],
        )
        if result and set_status:
            self.status.color_temperature = temperature
        return result

    async def set_fan_speed(
        self, speed: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the set fan speed device command."""
        if speed < 0:
            raise ValueError("value must be >= 0.")

        result = await self.command(
            component_id, Capability.fan_speed, Command.set_fan_speed, [speed]
        )
        if result and set_status:
            self.status.fan_speed = speed
            self.status.switch = speed > 0
        return result

    async def set_hue(
        self, hue: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the set hue device command."""
        if not 0 <= hue <= 100:
            raise ValueError("hue must be scaled between 0-100.")

        result = await self.command(
            component_id, Capability.color_control, Command.set_hue, [hue]
        )
        if result and set_status:
            self.status.hue = hue
        return result

    async def set_level(
        self,
        level: int,
        duration: int = 0,
        set_status: bool = False,
        *,
        component_id: str = "main"
    ) -> bool:
        """Call the set level device command."""
        if not 0 <= level <= 100:
            raise ValueError("level must be scaled between 0-100.")
        if duration < 0:
            raise ValueError("duration must be >= 0.")

        result = await self.command(
            component_id, Capability.switch_level, Command.set_level, [level, duration]
        )
        if result and set_status:
            self.status.level = level
            self.status.switch = level > 0
        return result

    async def set_saturation(
        self, saturation: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the set saturation device command."""
        if not 0 <= saturation <= 100:
            raise ValueError("saturation must be scaled between 0-100.")

        result = await self.command(
            component_id, Capability.color_control, Command.set_saturation, [saturation]
        )
        if result and set_status:
            self.status.saturation = saturation
        return result

    async def set_thermostat_fan_mode(
        self, mode: str, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setThermostatFanMode device command."""
        capability = self.get_capability(
            Capability.thermostat_fan_mode, Capability.thermostat
        )
        result = await self.command(
            component_id, capability, Command.set_thermostat_fan_mode, [mode]
        )
        if result and set_status:
            self.status.thermostat_fan_mode = mode
        return result

    async def set_thermostat_mode(
        self, mode: str, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setThermostatMode deivce command."""
        capability = self.get_capability(
            Capability.thermostat_mode, Capability.thermostat
        )
        result = await self.command(
            component_id, capability, Command.set_thermostat_mode, [mode]
        )
        if result and set_status:
            self.status.thermostat_mode = mode
        return result

    async def set_cooling_setpoint(
        self, temperature: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setThermostatMode deivce command."""
        capability = self.get_capability(
            Capability.thermostat_cooling_setpoint, Capability.thermostat
        )
        result = await self.command(
            component_id, capability, Command.set_cooling_setpoint, [temperature]
        )
        if result and set_status:
            self.status.cooling_setpoint = temperature
        return result

    async def set_heating_setpoint(
        self, temperature: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setThermostatMode deivce command."""
        capability = self.get_capability(
            Capability.thermostat_heating_setpoint, Capability.thermostat
        )
        result = await self.command(
            component_id, capability, Command.set_heating_setpoint, [temperature]
        )
        if result and set_status:
            self.status.heating_setpoint = temperature
        return result

    async def switch_off(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the switch off device command."""
        result = await self.command(component_id, Capability.switch, Command.off)
        if result and set_status:
            self.status.switch = False
        return result

    async def switch_on(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the switch on device command."""
        result = await self.command(component_id, Capability.switch, Command.on)
        if result and set_status:
            self.status.switch = True
        return result

    async def lock(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the lock device command."""
        result = await self.command(component_id, Capability.lock, Command.lock)
        if result and set_status:
            self.status.update_attribute_value(Attribute.lock, "locked")
        return result

    async def unlock(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the unlock device command."""
        result = await self.command(component_id, Capability.lock, Command.unlock)
        if result and set_status:
            self.status.update_attribute_value(Attribute.lock, "unlocked")
        return result

    async def open(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the open device command."""
        capability = self.get_capability(
            Capability.door_control,
            Capability.window_shade,
            Capability.garage_door_control,
        )
        result = await self.command(component_id, capability, Command.open)
        if result and set_status:
            attribute = (
                Attribute.window_shade
                if capability == Capability.window_shade
                else Attribute.door
            )
            self.status.update_attribute_value(attribute, "opening")
        return result

    async def close(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the close device command."""
        capability = self.get_capability(
            Capability.door_control,
            Capability.window_shade,
            Capability.garage_door_control,
        )
        result = await self.command(component_id, capability, Command.close)
        if result and set_status:
            attribute = (
                Attribute.window_shade
                if capability == Capability.window_shade
                else Attribute.door
            )
            self.status.update_attribute_value(attribute, "closing")
        return result

    async def preset_position(self, *, component_id: str = "main") -> bool:
        """Call the close device command."""
        return await self.command(component_id, Capability.window_shade, Command.close)

    async def request_drlc_action(
        self,
        drlc_type: int,
        drlc_level: int,
        start: str,
        duration: int,
        reporting_period: int = None,
        *,
        set_status: bool = False,
        component_id: str = "main"
    ):
        """Call the drlc action command."""
        args = [drlc_type, drlc_level, start, duration]
        if reporting_period is not None:
            args.append(reporting_period)
        result = await self.command(
            component_id,
            Capability.demand_response_load_control,
            Command.request_drlc_action,
            args,
        )
        if result and set_status:
            data = {
                "duration": duration,
                "drlcLevel": drlc_level,
                "start": start,
                "override": False,
            }
            self.status.apply_attribute_update(
                component_id,
                Capability.demand_response_load_control,
                Attribute.drlc_status,
                data,
            )
        return result

    async def override_drlc_action(
        self, value: bool, *, set_status: bool = False, component_id: str = "main"
    ):
        """Call the drlc override command."""
        result = await self.command(
            component_id,
            Capability.demand_response_load_control,
            Command.override_drlc_action,
            [value],
        )
        if result and set_status:
            data = self.status.drlc_status
            if not data:
                data = {}
                self.status.apply_attribute_update(
                    component_id,
                    Capability.demand_response_load_control,
                    Attribute.drlc_status,
                    data,
                )
            data["override"] = value
        return result

    async def execute(
        self, command: str, args: Dict = None, *, component_id: str = "main"
    ):
        """Call the execute command."""
        command_args = [command]
        if args:
            command_args.append(args)
        return await self.command(
            component_id, Capability.execute, Command.execute, command_args
        )

    async def set_air_conditioner_mode(
        self, mode: str, *, set_status: bool = False, component_id: str = "main"
    ):
        """Call the set air conditioner mode command."""
        result = await self.command(
            component_id,
            Capability.air_conditioner_mode,
            Command.set_air_conditioner_mode,
            [mode],
        )
        if result and set_status:
            self.status.update_attribute_value(Attribute.air_conditioner_mode, mode)
        return result

    async def set_fan_mode(
        self, mode: str, *, set_status: bool = False, component_id: str = "main"
    ):
        """Call the setFanMode command."""
        result = await self.command(
            component_id,
            Capability.air_conditioner_fan_mode,
            Command.set_fan_mode,
            [mode],
        )
        if result and set_status:
            self.status.update_attribute_value(Attribute.fan_mode, mode)
        return result

    async def set_air_flow_direction(
        self, direction: str, *, set_status: bool = False, component_id: str = "main"
    ):
        """Call the setAirFlowDirection command."""
        result = await self.command(
            component_id,
            Capability.air_flow_direction,
            Command.set_air_flow_direction,
            [direction],
        )
        if result and set_status:
            self.status.update_attribute_value(Attribute.air_flow_direction, direction)
        return result

    async def mute(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the mute command."""
        result = await self.command(component_id, Capability.audio_mute, Command.mute)
        if result and set_status:
            self.status.mute = True
        return result

    async def unmute(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the unmute command."""
        result = await self.command(component_id, Capability.audio_mute, Command.unmute)
        if result and set_status:
            self.status.mute = False
        return result

    async def set_volume(
        self, volume: int, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setVolume command."""
        result = await self.command(
            component_id, Capability.audio_volume, Command.set_volume, [volume]
        )
        if result and set_status:
            self.status.volume = volume
        return result

    async def volume_up(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the volumeUp command."""
        result = await self.command(
            component_id, Capability.audio_volume, Command.volume_up
        )
        if result and set_status:
            self.status.volume = min(self.status.volume + 1, 100)
        return result

    async def volume_down(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the volumeDown command."""
        result = await self.command(
            component_id, Capability.audio_volume, Command.volume_down
        )
        if result and set_status:
            self.status.volume = max(self.status.volume - 1, 0)
        return result

    async def play(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the play command."""
        result = await self.command(
            component_id, Capability.media_playback, Command.play
        )
        if result and set_status:
            self.status.playback_status = "play"
        return result

    async def pause(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the pause command."""
        result = await self.command(
            component_id, Capability.media_playback, Command.pause
        )
        if result and set_status:
            self.status.playback_status = "pause"
        return result

    async def stop(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the stop command."""
        result = await self.command(
            component_id, Capability.media_playback, Command.stop
        )
        if result and set_status:
            self.status.playback_status = "stop"
        return result

    async def fast_forward(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the fastForward command."""
        result = await self.command(
            component_id, Capability.media_playback, Command.fast_forward
        )
        if result and set_status:
            self.status.playback_status = "fast forward"
        return result

    async def rewind(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the rewind command."""
        result = await self.command(
            component_id, Capability.media_playback, Command.rewind
        )
        if result and set_status:
            self.status.playback_status = "rewind"
        return result

    async def set_input_source(
        self, source: str, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setInputSource command."""
        result = await self.command(
            component_id,
            Capability.media_input_source,
            Command.set_input_source,
            [source],
        )
        if result and set_status:
            self.status.input_source = source
        return result

    async def set_playback_shuffle(
        self, shuffle: bool, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setPlaybackShuffle command."""
        shuffle_value = bool_to_value(Attribute.playback_shuffle, shuffle)
        result = await self.command(
            component_id,
            Capability.media_playback_shuffle,
            Command.set_playback_shuffle,
            [shuffle_value],
        )
        if result and set_status:
            self.status.playback_shuffle = shuffle
        return result

    async def set_repeat(
        self, repeat: str, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setPlaybackRepeatMode command."""
        result = await self.command(
            component_id,
            Capability.media_playback_repeat,
            Command.set_playback_repeat_mode,
            [repeat],
        )
        if result and set_status:
            self.status.playback_repeat_mode = repeat
        return result

    async def set_tv_channel(
        self, channel: str, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the setTvChannel command."""
        result = await self.command(
            component_id, Capability.tv_channel, Command.set_tv_channel, [channel]
        )
        if result and set_status:
            self.status.tv_channel = channel
        return result

    async def channel_up(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the channelUp command."""
        return await self.command(
            component_id, Capability.tv_channel, Command.channel_up
        )

    async def channel_down(
        self, set_status: bool = False, *, component_id: str = "main"
    ) -> bool:
        """Call the channelDown command."""
        return await self.command(
            component_id, Capability.tv_channel, Command.channel_down
        )

    @property
    def status(self):
        """Get the status entity of the device."""
        return self._status
