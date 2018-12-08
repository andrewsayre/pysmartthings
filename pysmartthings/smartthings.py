"""Define the SmartThings Cloud API."""

import logging
from threading import Thread
from .api import API
from .device import Device
from .location import Location

_LOGGER = logging.getLogger(__name__)


class SmartThings:
    """Define a class for interacting with the SmartThings Cloud API."""

    def __init__(self, token):
        """
        Initialize the API.

        :param token: The personal access token used to authenticate to the API
        :type token: str
        """
        self._api = API(token)
        self._locations = []
        self._devices = []
        self._load()

    def _load(self):
        # Get locations
        resp = self._api.get_locations()
        self._locations.clear()
        for entity in resp["items"]:
            self._locations.append(Location(self._api, entity))
        # Get devices
        resp = self._api.get_devices()
        self._devices.clear()
        for entity in resp["items"]:
            self._devices.append(Device(self._api, entity))

    def update(self):
        """Retrieve the latest status for all devices."""
        threads = []
        for dev in self.devices:
            thread = Thread(target=dev.update)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return True

    @property
    def locations(self):
        """Get locations."""
        return self._locations

    @property
    def devices(self):
        """Get loaded devices."""
        return self._devices
