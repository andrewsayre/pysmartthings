"""Define the SmartThing location."""

from typing import List, Optional

from .api import Api
from .entity import Entity
from .room import RoomEntity


class Location:
    """Represents a SmartThings Location."""

    def __init__(self):
        """Initialize a new location."""
        self._name = None
        self._location_id = None
        self._latitude = None
        self._longitude = None
        self._region_radius = None
        self._temperature_scale = None
        self._locale = None
        self._country_code = None
        self._timezone_id = None

    def apply_data(self, data: dict):
        """Apply the given data structure to the location."""
        self._name = data["name"]
        self._location_id = data["locationId"]
        self._latitude = data.get("latitude", None)
        self._longitude = data.get("longitude", None)
        self._region_radius = data.get("regionRadius", None)
        self._temperature_scale = data.get("temperatureScale", None)
        self._locale = data.get("locale", None)
        self._country_code = data.get("countryCode", None)
        self._timezone_id = data.get("timeZoneId", None)

    @property
    def name(self) -> str:
        """Get nickname given for the location."""
        return self._name

    @property
    def location_id(self) -> str:
        """Get the ID of the location."""
        return self._location_id

    @property
    def latitude(self) -> float:
        """Get the geographical latitude."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Get the geographical longitude."""
        return self._longitude

    @property
    def region_radius(self) -> int:
        """Get the radius in meters which defines this location."""
        return self._region_radius

    @property
    def temperature_scale(self) -> str:
        """Get the temperature scale of the location (F or C)."""
        return self._temperature_scale

    @property
    def locale(self) -> str:
        """Get the IETF BCP 47 language tag of the location."""
        return self._locale

    @property
    def country_code(self) -> str:
        """Get the country code of the location."""
        return self._country_code

    @property
    def timezone_id(self) -> str:
        """Get the ID matching the Java Time Zone ID of the location."""
        return self._timezone_id


class LocationEntity(Entity, Location):
    """Define a location entity."""

    def __init__(
        self, api: Api, data: Optional[dict] = None, location_id: Optional[str] = None
    ):
        """Create a new instance of the LocationEntity."""
        Entity.__init__(self, api)
        Location.__init__(self)
        if data:
            self.apply_data(data)
        if location_id:
            self._location_id = location_id

    async def refresh(self):
        """Refresh the location information."""
        data = await self._api.get_location(self._location_id)
        if data:
            self.apply_data(data)

    async def save(self):
        """Location does not support updating at this time."""
        raise NotImplementedError("Location does not support updating at this time.")

    async def rooms(self) -> List[RoomEntity]:
        """Get the rooms contained within the location."""
        resp = await self._api.get_rooms(self._location_id)
        return [RoomEntity(self._api, entity) for entity in resp]
