"""Defines the rooms module."""
from typing import Dict, Optional

from .api import Api
from .entity import Entity


class Room:
    """Defines a SmartThings room."""

    def __init__(self):
        """Initialize the room."""
        self._room_id = None
        self._location_id = None
        self._name = None
        self._background_image = None

    def apply_data(self, data: dict):
        """Apply the data structure to the class."""
        self._room_id = data["roomId"]
        self._location_id = data["locationId"]
        self._name = data["name"]
        self._background_image = data["backgroundImage"]

    def to_data(self) -> dict:
        """Get a data structure representing this entity."""
        data = {
            "name": self._name,
            "backgroundImage": self._background_image,
        }
        return data

    @property
    def room_id(self) -> str:
        """Get the id of the room."""
        return self._room_id

    @room_id.setter
    def room_id(self, value: str):
        """Set the id of the room."""
        self._room_id = value

    @property
    def location_id(self) -> str:
        """Get the location id the room is part of."""
        return self._location_id

    @location_id.setter
    def location_id(self, value: str):
        """Set the location id of the room."""
        self._location_id = value

    @property
    def name(self) -> str:
        """Get the name of the room."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name of the room."""
        self._name = value

    @property
    def background_image(self) -> str:
        """Get the background image of the room."""
        return self._background_image

    @background_image.setter
    def background_image(self, value: str):
        """Set the background image."""
        self._background_image = value


class RoomEntity(Room, Entity):
    """Defines a SmartThings room entity."""

    def __init__(
        self,
        api: Api,
        data: Optional[Dict] = None,
        *,
        location_id: str = None,
        room_id: str = None
    ):
        """Initialize the room."""
        Entity.__init__(self, api)
        Room.__init__(self)
        if data:
            self.apply_data(data)
        if location_id:
            self._location_id = location_id
        if room_id:
            self._room_id = room_id

    async def refresh(self):
        """Refresh the room."""
        data = await self._api.get_room(self._location_id, self._room_id)
        if data:
            self.apply_data(data)

    async def save(self):
        """Save changes to the room."""
        data = await self._api.update_room(
            self._location_id, self._room_id, self.to_data()
        )
        if data:
            self.apply_data(data)
