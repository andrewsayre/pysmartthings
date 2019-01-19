"""Defines a SmartThings device."""
import colorsys
from enum import Enum
import re
from typing import Any, Dict, Optional, Sequence

from .api import Api
from .entity import Entity


def hs_to_hex(hue: float, saturation: float) -> str:
    """Convert hue and saturation to a string hex color."""
    rgb = colorsys.hsv_to_rgb(hue/100, saturation/100, 100)
    return '#{:02x}{:02x}{:02x}'.format(
        round(rgb[0]), round(rgb[1]), round(rgb[2])).upper()


def hex_to_hs(color_hex: str) -> (int, int):
    """Convert a string hex color to hue and saturation components."""
    color_hex = color_hex.lstrip('#')
    rgb = [int(color_hex[i:i + len(color_hex) // 3], 16)/255.0
           for i in range(0, len(color_hex), len(color_hex) // 3)]
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    return round(hsv[0]*100, 3), round(hsv[1]*100, 3)


COLOR_HEX_MATCHER = re.compile('^#[A-Fa-f0-9]{6}$')


class Attribute:
    """Define common attributes."""

    acceleration = 'acceleration'
    color = 'color'
    color_temperature = 'colorTemperature'
    contact = 'contact'
    fan_speed = 'fanSpeed'
    filter_status = 'filterStatus'
    hue = 'hue'
    level = 'level'
    motion = 'motion'
    mute = 'mute'
    presence = 'presence'
    saturation = 'saturation'
    sound = 'sound'
    switch = 'switch'
    tamper = 'tamper'
    valve = 'valve'
    water = 'water'


class Capability:
    """Define common capabilities."""

    color_control = 'colorControl'
    color_temperature = 'colorTemperature'
    fan_speed = 'fanSpeed'
    light = 'light'
    motion_sensor = 'motionSensor'
    switch = 'switch'
    switch_level = 'switchLevel'


class Command:
    """Define common commands."""

    off = 'off'
    on = 'on'
    set_color = 'setColor'
    set_color_temperature = 'setColorTemperature'
    set_fan_speed = 'setFanSpeed'
    set_hue = 'setHue'
    set_level = 'setLevel'
    set_saturation = 'setSaturation'


class DeviceType(Enum):
    """Define the device type."""

    UNKNOWN = 'UNKNOWN'
    DTH = 'DTH'
    ENDPOINT_APP = 'ENDPOINT_APP'


ATTRIBUTE_ON_VALUES = {
    Attribute.acceleration: 'active',
    Attribute.contact: 'open',
    Attribute.filter_status: 'replace',
    Attribute.motion: 'active',
    Attribute.mute: 'muted',
    Attribute.presence: 'present',
    Attribute.sound: 'detected',
    Attribute.switch: 'on',
    Attribute.tamper: 'detected',
    Attribute.valve: 'open',
    Attribute.water: 'wet'
}


class Device:
    """Represents a SmartThings device."""

    def __init__(self):
        """Initialize a new device."""
        self._device_id = None
        self._name = None
        self._label = None
        self._location_id = None
        self._type = DeviceType.UNKNOWN
        self._device_type_id = None
        self._device_type_name = None
        self._device_type_network = None
        self._components = {}
        self._capabilities = []

    def apply_data(self, data: dict):
        """Apply the given data dictionary."""
        self._device_id = data['deviceId']
        self._name = data['name']
        self._label = data['label']
        self._location_id = data['locationId']
        self._type = DeviceType(data['type'])
        self._components.clear()
        self._capabilities.clear()
        for comp_data in data['components']:
            capabilities = []
            for capability_data in comp_data['capabilities']:
                capability_id = capability_data['id']
                capabilities.append(capability_id)
                if id not in self._capabilities:
                    self._capabilities.append(capability_id)
            self._components[comp_data['id']] = capabilities
        if self._type is DeviceType.DTH:
            dth = data['dth']
            self._device_type_id = dth["deviceTypeId"]
            self._device_type_name = dth["deviceTypeName"]
            self._device_type_network = dth["deviceNetworkType"]

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
    def type(self) -> DeviceType:
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


class DeviceStatus:
    """Define the device status."""

    def __init__(self, api: Api, device_id: str, data=None):
        """Create a new instance of the DeviceStatusEntity class."""
        self._api = api
        self._attributes = {}
        self._device_id = device_id
        if data:
            self.apply_data(data)

    @property
    def device_id(self) -> str:
        """Get the device id."""
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        """Set the device id."""
        self._device_id = value

    def apply_data(self, data: dict):
        """Apply the values from the given data structure."""
        self._attributes.clear()
        for capabilities in data['components'].values():
            for attributes in capabilities.values():
                for attribute, value in attributes.items():
                    self._attributes[attribute] = value['value']

    def apply_attribute_update(self, component_id: str, capability: str,
                               attribute: str, value: Any):
        """Apply an update to a specific attribute."""
        # component_id and capability future usage.
        self._attributes[attribute] = value

    def is_on(self, attribute: str) -> bool:
        """Determine if a specific attribute contains an on/True value."""
        if attribute not in ATTRIBUTE_ON_VALUES:
            return bool(self._attributes.get(attribute))
        return self._attributes.get(attribute) == \
            ATTRIBUTE_ON_VALUES[attribute]

    async def refresh(self):
        """Refresh the values of the entity."""
        data = await self._api.get_device_status(self.device_id)
        if data:
            self.apply_data(data)

    @property
    def attributes(self):
        """Get all of the attribute values."""
        return self._attributes

    @property
    def color(self) -> Optional[str]:
        """Get the color attribute."""
        return self._attributes.get(Attribute.color)

    @color.setter
    def color(self, value: str):
        """Set the color attribute."""
        if not COLOR_HEX_MATCHER.match(value):
            raise ValueError(
                "value was not a properly formatted color hex, i.e. #000000.")
        self._attributes[Attribute.color] = value

    @property
    def color_temperature(self) -> int:
        """Get the color temperature attribute."""
        return int(self._attributes.get(Attribute.color_temperature, 1))

    @color_temperature.setter
    def color_temperature(self, value: int):
        """Set the color temperature attribute."""
        if not 1 <= value <= 30000:
            raise ValueError("value must be scaled between 1-30000.")
        self._attributes[Attribute.color_temperature] = value

    @property
    def fan_speed(self) -> int:
        """Get the fan speed attribute."""
        return int(self._attributes.get(Attribute.fan_speed, 0))

    @fan_speed.setter
    def fan_speed(self, value: int):
        """Set the fan speed attribute."""
        if value < 0:
            raise ValueError("value must be >= 0.")
        self._attributes[Attribute.fan_speed] = value

    @property
    def hue(self) -> float:
        """Get the hue attribute, scaled 0-100."""
        return float(self._attributes.get(Attribute.hue, 0))

    @hue.setter
    def hue(self, value: float):
        """Set the hue attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self._attributes[Attribute.hue] = value

    @property
    def level(self) -> int:
        """Get the level attribute, scaled 0-100."""
        return int(self._attributes.get(Attribute.level, 0))

    @level.setter
    def level(self, value: int):
        """Set the level of the attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self._attributes[Attribute.level] = value

    @property
    def saturation(self) -> float:
        """Get the saturation attribute, scaled 0-100."""
        return float(self._attributes.get(Attribute.saturation, 0))

    @saturation.setter
    def saturation(self, value: float):
        """Set the saturation attribute, scaled 0-100."""
        if not 0 <= value <= 100:
            raise ValueError("value must be scaled between 0-100.")
        self._attributes[Attribute.saturation] = value

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
        self._attributes[Attribute.switch] = \
            ATTRIBUTE_ON_VALUES[Attribute.switch] if value else 'off'


class DeviceEntity(Entity, Device):
    """Define a device entity."""

    def __init__(self, api: Api, data: Optional[dict] = None,
                 device_id: Optional[str] = None):
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

    async def command(self, capability, command, args=None) -> bool:
        """Execute a command on the device."""
        response = await self._api.post_device_command(
            self._device_id, capability, command, args)
        return response == {}

    async def set_color(
            self, hue: Optional[float] = None,
            saturation: Optional[float] = None,
            color_hex: Optional[str] = None,
            set_status: bool = False) -> bool:
        """Call the set color command."""
        color_map = {}
        if color_hex:
            if not COLOR_HEX_MATCHER.match(color_hex):
                raise ValueError("color_hex was not a properly formatted "
                                 "color hex, i.e. #000000.")
            color_map['hex'] = color_hex
        else:
            if not 0 <= hue <= 100:
                raise ValueError("hue must be scaled between 0-100.")
            if not 0 <= saturation <= 100:
                raise ValueError("saturation must be scaled between 0-100.")
            color_map['hue'] = hue
            color_map['saturation'] = saturation

        result = await self.command(
            Capability.color_control, Command.set_color, [color_map])
        if result and set_status:
            if color_hex:
                self.status.color = color_hex
                self.status.hue, self.status.saturation = hex_to_hs(color_hex)
            else:
                self.status.color = hs_to_hex(hue, saturation)
                self.status.hue = hue
                self.status.saturation = saturation
        return result

    async def set_color_temperature(self, temperature: int,
                                    set_status: bool = False) -> bool:
        """Call the color temperature device command."""
        if not 1 <= temperature <= 30000:
            raise ValueError("temperature must be scaled between 1-30000.")

        result = await self.command(
            Capability.color_temperature, Command.set_color_temperature,
            [temperature])
        if result and set_status:
            self.status.color_temperature = temperature
        return result

    async def set_fan_speed(
            self, speed: int, set_status: bool = False) -> bool:
        """Call the set fan speed device command."""
        if speed < 0:
            raise ValueError("value must be >= 0.")

        result = await self.command(
            Capability.fan_speed, Command.set_fan_speed, [speed])
        if result and set_status:
            self.status.fan_speed = speed
            self.status.switch = speed > 0
        return result

    async def set_hue(self, hue: int, set_status: bool = False) -> bool:
        """Call the set hue device command."""
        if not 0 <= hue <= 100:
            raise ValueError("hue must be scaled between 0-100.")

        result = await self.command(
            Capability.color_control, Command.set_hue, [hue])
        if result and set_status:
            self.status.hue = hue
        return result

    async def set_level(self, level: int, duration: int = 0,
                        set_status: bool = False) -> bool:
        """Call the set level device command."""
        if not 0 <= level <= 100:
            raise ValueError("level must be scaled between 0-100.")
        if duration < 0:
            raise ValueError("duration must be >= 0.")

        result = await self.command(
            Capability.switch_level, Command.set_level, [level, duration])
        if result and set_status:
            self.status.level = level
            self.status.switch = level > 0
        return result

    async def set_saturation(
            self, saturation: int, set_status: bool = False) -> bool:
        """Call the set saturation device command."""
        if not 0 <= saturation <= 100:
            raise ValueError("saturation must be scaled between 0-100.")

        result = await self.command(
            Capability.color_control, Command.set_saturation, [saturation])
        if result and set_status:
            self.status.saturation = saturation
        return result

    async def switch_off(self, set_status: bool = False) -> bool:
        """Call the switch off device command."""
        result = await self.command(Capability.switch, Command.off)
        if result and set_status:
            self.status.switch = False
        return result

    async def switch_on(self, set_status: bool = False) -> bool:
        """Call the switch on device command."""
        result = await self.command(Capability.switch, Command.on)
        if result and set_status:
            self.status.switch = True
        return result

    @property
    def status(self):
        """Get the status entity of the device."""
        return self._status
