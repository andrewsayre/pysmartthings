"""Define the SmartThings Cloud API."""

from .api import API
from .device import Device
from .location import Location


class SmartThings:
    """Define a class for interacting with the SmartThings Cloud API."""

    def __init__(self, token):
        """
        Initialize the API.

        :param token: The personal access token used to authenticate to the API
        :type token: str
        """
        self._api = API(token)

    def locations(self):
        """Retrieve SmartThings locations."""
        resp = self._api.get_locations()
        return [Location(self._api, entity) for entity in resp["items"]]

    def devices(self):
        """Retrieve SmartThings devices."""
        resp = self._api.get_devices()
        return [Device(self._api, entity) for entity in resp["items"]]
