"""Defines a SmartThings device."""

from enum import Enum
from typing import Dict, Optional, Sequence

from .api import API
from .entity import Entity


class Capability:
    """Define common capabilities."""

    switch = 'switch'
    switch_level = 'switchLevel'
    light = 'light'
    motion_sensor = 'motionSensor'


class DeviceType(Enum):
    """Define the device type."""

    UNKNOWN = 'UNKNOWN'
    DTH = 'DTH'
    ENDPOINT_APP = 'ENDPOINT_APP'


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

    def __init__(self, api: API, device_id: str, data=None):
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

    def refresh(self):
        """Refresh the values of the entity."""
        data = self._api.get_device_status(self.device_id)
        if data:
            self.apply_data(data)

    @property
    def attributes(self):
        """Get all of the attribute values."""
        return self._attributes

    @property
    def switch(self) -> bool:
        """Get the switch attribute."""
        return self._attributes.get('switch', None) == 'on'

    @property
    def level(self) -> int:
        """Get the level attribute."""
        return int(self._attributes.get('level', 0))

    @property
    def motion(self) -> bool:
        """Get the motion attribute."""
        return self._attributes.get('motion', None) == 'on'


class DeviceEntity(Entity, Device):
    """Define a device entity."""

    def __init__(self, api: API, data: Optional[dict] = None,
                 device_id: Optional[str] = None):
        """Create a new instance of the DeviceEntity class."""
        Entity.__init__(self, api)
        Device.__init__(self)
        if data:
            self.apply_data(data)
        if device_id:
            self._device_id = device_id
        self._status = DeviceStatus(api, self._device_id)

    def refresh(self):
        """Refresh the device information using the API."""
        data = self._api.get_device(self._device_id)
        if data:
            self.apply_data(data)
        self._status.device_id = self._device_id

    def save(self):
        """Save the changes made to the device."""
        raise NotImplementedError

    def command(self, capability, command, args=None):
        """Execute a command on the device."""
        response = self._api.post_command(
            self._device_id, capability, command, args)
        return response == {}

    def switch_on(self) -> bool:
        """Turn on the device."""
        return self.command(Capability.switch, "on")

    def switch_off(self) -> bool:
        """Turn on the device."""
        return self.command(Capability.switch, "off")

    def set_level(self, level: int, duration: int) -> bool:
        """Set the level of the device."""
        return self.command(Capability.switch_level,
                            'setLevel', [level, duration])

    @property
    def status(self):
        """Get the status entity of the device."""
        return self._status
