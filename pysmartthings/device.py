"""Defines a SmartThings device"""
from . import smartthings


class Device:
    """Represents a SmartThings device"""
    def __init__(self, parent, entity):
        """
        Initialize a new device

        :param parent: The parent API service
        :type parent: smartthings.SmartThings

        :param entity: The json representation of the device form the API
        """
        self._parent = parent
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
                    self._capabilities.append(capability["id"])
                break

    def update(self):
        data = self._parent._update_device(self.device_id)
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

    @property
    def device_id(self):
        return self._device_id

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def location_id(self):
        return self._location_id

    @property
    def type(self):
        return self._type

    @property
    def device_type_id(self):
        return self._device_type_id

    @property
    def device_type_name(self):
        return self._device_type_name

    @property
    def device_type_network(self):
        return self._device_type_network

    @property
    def capabilities(self):
        return self._capabilities

    @property
    def status(self):
        return self._status
