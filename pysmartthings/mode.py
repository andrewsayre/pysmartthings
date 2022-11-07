"""Define the SmartThing location mode."""

from typing import Dict, List, Optional

from .api import Api
from .entity import Entity


class Mode:
    """Represents a SmartThings Mode."""

    def __init__(self):
        """Initialize a new mode."""
        self._mode_id = None
        self._location_id = None
        self._name = None
        self._label = None
        self._allowed = None
        self._last_modified = None

    def apply_data(self, data: dict):
        """Apply the given data structure to the mode."""
        self._mode_id = data["id"]
        self._location_id = data["locationId"]
        self._name = data["name"]
        self._label = data["label"]
        self._allowed = data["allowed"]
        self._last_modified = data["lastModified"]

    def to_data(self) -> dict:
        """Get a data structure representing this entity."""
        data = {
            "id": self._mode_id,
            "locationId": self._location_id,
            "name": self._name,
            "label": self._label,
            "allowed": self._allowed,
            "lastModified": self._last_modified,
        }
        return data

    @property
    def mode_id(self) -> str:
        """Get the ID of the mode."""
        return self._mode_id

    @property
    def location_id(self) -> str:
        """Get the location id the mode is part of."""
        return self._location_id

    @location_id.setter
    def location_id(self, value: str):
        """Set the location id the mode is part of."""
        self._location_id = value

    @property
    def name(self) -> str:
        """Get nickname given for the mode."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name of the mode."""
        self._name = value

    @property
    def label(self) -> str:
        """Get label given for the mode."""
        return self._label

    @label.setter
    def label(self, value: str):
        """Set the label of the mode."""
        self._label = value

    @property
    def allowed(self) -> str:
        """Get the allowed settings of the mode."""
        return self._allowed

    @property
    def last_modified(self) -> int:
        """Get the last modified timestamp of the mode."""
        return self._last_modified


class ModeEntity(Entity, Mode):
    """Define a mode entity."""

    def __init__(
        self,
        api: Api,
        data: Optional[Dict] = None,
        *,
        location_id: str = None,
        mode_id: str = None
    ):
        """Create a new instance of the ModeEntity."""
        Entity.__init__(self, api)
        Mode.__init__(self)
        if data:
            self.apply_data(data)
        if mode_id:
            self._mode_id = mode_id
        if location_id:
            self._location_id = location_id

    async def refresh(self):
        """Refresh the current mode information."""
        data = await self._api.get_mode(self._location_id, self._mode_id)
        if data:
            data["locationId"] = self._location_id
            self.apply_data(data)

    async def save(self):
        """Save changes to the mode."""
        data = await self._api.update_mode(
            self._location_id, self._mode_id, self.to_data()
        )
        if data:
            self.apply_data(data)
