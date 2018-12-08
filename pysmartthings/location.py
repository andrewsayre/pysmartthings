"""Define the SmartThing location."""


class Location:
    """Represents a SmartThings Location."""

    def __init__(self, api, entity):
        """Initialize a new location."""
        self._api = api
        self._name = entity["name"]
        self._location_id = entity["locationId"]

    @property
    def name(self):
        """Get the SmartThings location name."""
        return self._name

    @property
    def location_id(self):
        """Get the SmartThings location id."""
        return self._location_id
