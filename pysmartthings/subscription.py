"""Define the subscription module."""

from enum import Enum
from typing import Any, Optional

from .api import Api
from .entity import Entity


class SourceType(Enum):
    """Define the source type of a subscription."""

    UNKNOWN = "UNKNOWN"
    DEVICE = "DEVICE"
    CAPABILITY = "CAPABILITY"


class Subscription:
    """Define the subscription class."""

    def __init__(self):
        """Initialize a new instance of the subscription class."""
        self._subscription_id = None
        self._installed_app_id = None
        self._source_type = SourceType.UNKNOWN
        self._capability = "*"
        self._attribute = "*"
        self._value = "*"
        self._state_change_only = True
        self._subscription_name = None
        # Capability-specific attributes
        self._location_id = None
        # Device-specific attributes
        self._device_id = None
        self._component_id = None

    def apply_data(self, data: dict):
        """Set the states of the app with the supplied data."""
        self._subscription_id = data["id"]
        self._installed_app_id = data["installedAppId"]
        self._source_type = SourceType(data["sourceType"])
        if self._source_type is SourceType.CAPABILITY:
            capability = data["capability"]
            self._location_id = capability["locationId"]
            self._capability = capability["capability"]
            self._attribute = capability.get("attribute", "*")
            self._value = capability.get("value", "*")
            self._state_change_only = capability.get("stateChangeOnly", True)
            self._subscription_name = capability.get("subscriptionName", None)
        if self._source_type is SourceType.DEVICE:
            device = data["device"]
            self._device_id = device["deviceId"]
            self._component_id = device.get("componentId", "*")
            self._capability = device.get("capability", "*")
            self._attribute = device.get("attribute", "*")
            self._value = device.get("value", "*")
            self._state_change_only = device.get("stateChangeOnly", True)
            self._subscription_name = device.get("subscriptionName", None)

    def to_data(self) -> dict:
        """Get a data structure representing this entity."""
        data = {"sourceType": self._source_type.value}
        if self._source_type is SourceType.CAPABILITY:
            capability = {
                "locationId": self._location_id,
                "capability": self._capability,
            }
            if self._attribute and self._attribute != "*":
                capability["attribute"] = self._attribute
            if self._value and self._value != "*":
                capability["value"] = self._value
            if not self._state_change_only:
                capability["stateChangeOnly"] = False
            if self._subscription_name:
                capability["subscriptionName"] = self._subscription_name
            data["capability"] = capability
        if self._source_type is SourceType.DEVICE:
            device = {
                "deviceId": self._device_id,
                "stateChangeOnly": self._state_change_only,
            }
            if self._component_id and self._component_id != "*":
                device["componentId"] = self._component_id
            if self._capability and self._capability != "*":
                device["capability"] = self._capability
            if self._attribute and self._attribute != "*":
                device["attribute"] = self._attribute
            if self._value and self._value != "*":
                device["value"] = self._value
            if self._subscription_name:
                device["subscriptionName"] = self._subscription_name
            data["device"] = device
        return data

    @property
    def subscription_id(self) -> str:
        """Get the id of the subscription."""
        return self._subscription_id

    @property
    def installed_app_id(self) -> str:
        """Get the id of the subscribing app."""
        return self._installed_app_id

    @installed_app_id.setter
    def installed_app_id(self, value: str):
        """Set the id of the subscripting app."""
        self._installed_app_id = value

    @property
    def source_type(self) -> SourceType:
        """Get the type of the event that is being subscribed to."""
        return self._source_type

    @source_type.setter
    def source_type(self, value: Any):
        """Set the typ eof event that is being subscribed to."""
        self._source_type = SourceType(value)

    @property
    def capability(self) -> str:
        """Get the name of the capability that is subscribed."""
        return self._capability

    @capability.setter
    def capability(self, value: str):
        """Get the name of the capability that is subscribed."""
        self._capability = value

    @property
    def attribute(self) -> str:
        """Get the name of the capabilities attribute or * for all."""
        return self._attribute

    @attribute.setter
    def attribute(self, value: str):
        """Set the name of the capabilities attribute or * for all."""
        self._attribute = value

    @property
    def value(self) -> str:
        """Get the value for that will trigger the subscription."""
        return self._value

    @value.setter
    def value(self, value: str):
        """Set the value for that will trigger the subscription."""
        self._value = value

    @property
    def state_change_only(self) -> bool:
        """Get to execute only on a state change."""
        return self._state_change_only

    @state_change_only.setter
    def state_change_only(self, value: bool):
        """Set to execute only on a state change."""
        self._state_change_only = value

    @property
    def subscription_name(self) -> str:
        """Get a name for the subscription."""
        return self._subscription_name

    @subscription_name.setter
    def subscription_name(self, value: str):
        """Set a name for the subscription."""
        self._subscription_name = value

    @property
    def location_id(self) -> str:
        """Get the location id that both the app and source device are in."""
        return self._location_id

    @location_id.setter
    def location_id(self, value: str):
        """Set the location id that both the app and source device are in."""
        self._location_id = value

    @property
    def device_id(self):
        """Get the GUID of the device that is subscribed to."""
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        """Set the GUID of the device that is subscribed to."""
        self._device_id = value

    @property
    def component_id(self) -> str:
        """Get the component ID on the device that is subscribed to."""
        return self._component_id

    @component_id.setter
    def component_id(self, value: str):
        """Set the component ID on the device that is subscribed to."""
        self._component_id = value


class SubscriptionEntity(Entity, Subscription):
    """Define a subscription entity."""

    def __init__(self, api: Api, data: Optional[dict] = None):
        """Create a new instance of the SubscriptionEntity class."""
        Entity.__init__(self, api)
        Subscription.__init__(self)
        if data:
            self.apply_data(data)

    async def refresh(self):
        """Refresh the subscription information using the API."""
        data = await self._api.get_subscription(
            self._installed_app_id, self._subscription_id
        )
        self.apply_data(data)

    async def save(self):
        """Subscriptions cannot be updated."""
        raise NotImplementedError
