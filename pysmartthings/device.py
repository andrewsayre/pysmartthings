"""Defines a SmartThings device."""

from types import MethodType


class Device:
    """Represents a SmartThings device."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, api, entity):
        """
        Initialize a new device.

        :param api: The API service
        :type api: API

        :param entity: The json representation of the device form the API
        """
        self._api = api
        self._device_id = entity["deviceId"]
        self._name = entity["name"]
        self._label = entity["label"]
        self._location_id = entity["locationId"]
        self._type = entity["type"]
        self._status = {}

        if self._type == "DTH":
            dth = entity["dth"]
            self._device_type_id = dth["deviceTypeId"]
            self._device_type_name = dth["deviceTypeName"]
            self._device_type_network = dth["deviceNetworkType"]

        self._capabilities = []
        for component in entity["components"]:
            if component["id"] == "main":
                for capability in component["capabilities"]:
                    capability_id = capability["id"]
                    self._capabilities.append(capability_id)
                    Device._add_device_commands(capability_id, self)
                break

    def update(self):
        """Update the status of the device."""
        data = self._api.get_device_status(self.device_id)
        if data is None:
            return False
        for key, value in data.items():
            if key == "switchLevel":
                self._status["switchLevel"] = value["level"]["value"]
            elif key == "switch":
                self._status["switch"] = value["switch"]["value"]
            elif key == "light":
                self._status["light"] = value["switch"]["value"]
            elif key == "motionSensor":
                self._status["motionSensor"] = value["motion"]["value"]
        return True

    def command(self, capability, command, args=None):
        """Execute a command on the device."""
        response = self._api.post_command(
            self._device_id, capability, command, args)
        if response == {}:
            return True
        return False

    @property
    def device_id(self):
        """Get the SmartThings device id."""
        return self._device_id

    @property
    def name(self):
        """Get the SmartThings device name."""
        return self._name

    @property
    def label(self):
        """Get the SmartThings user assigned label."""
        return self._label

    @property
    def location_id(self):
        """Get the SmartThings location assigned to the device."""
        return self._location_id

    @property
    def type(self):
        """Get the SmartThings device type."""
        return self._type

    @property
    def device_type_id(self):
        """Get the SmartThings device type handler id."""
        return self._device_type_id

    @property
    def device_type_name(self):
        """Get the SmartThings device type handler name."""
        return self._device_type_name

    @property
    def device_type_network(self):
        """Get the SmartThings device type handler network."""
        return self._device_type_network

    @property
    def capabilities(self):
        """Get the SmartThings capabilities of the device."""
        return self._capabilities

    @property
    def status(self):
        """Get the capability status."""
        return self._status

    @staticmethod
    def _add_device_commands(capability, target):
        if capability == "switch":
            def switch_on(self):
                """Turn on the device."""
                return self.command("switch", "on")

            def switch_off(self):
                """Turn off the device."""
                return self.command("switch", "off")

            target.switch_on = MethodType(switch_on, target)
            target.switch_off = MethodType(switch_off, target)
        elif capability == "switchLevel":
            def set_level(self, level: int, duration: int):
                """Set the switch level of the device."""
                return self.command(
                    "switchLevel", "setLevel", [level, duration])

            target.set_level = MethodType(set_level, target)
