"""Defines the entity module."""

from .api import Api


class Entity:
    """Define an entity from the SmartThings API."""

    def __init__(self, api: Api):
        """Initialize a new instance of the entity."""
        self._api = api

    async def refresh(self):
        """Retrieve the latest values from the API."""
        raise NotImplementedError

    async def save(self):
        """Update or create the entity."""
        raise NotImplementedError
