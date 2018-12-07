"""Define the SmartThings Cloud API."""

import logging
from threading import Thread
from .api import API
from .device import Device

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
        self._devices = []
        self._get_devices()

    def _get_devices(self):
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
    def devices(self):
        """Get loaded devices."""
        return self._devices
