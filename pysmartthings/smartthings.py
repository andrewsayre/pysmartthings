"""Define the SmartThings Cloud API"""

import logging
import json
from threading import Thread
import requests
from . import device

_LOGGER = logging.getLogger(__name__)

API_BASE: str = 'https://api.smartthings.com/v1/'
API_RESOURCE_DEVICES: str = "devices"
API_RESOURCE_DEVICE_STATUS: str = "devices/{device_id}/components/main/status"


class SmartThings:
    """Define a class for interacting with the SmartThings Cloud API"""
    def __init__(self, token):
        """
        Initialize the API

        :param token: The personal access token used to authenticate to the API
        :type token: str
        """
        self._token = token
        self._devices = []
        self._create_devices()

    def _create_devices(self):
        resp = self._get_request(API_RESOURCE_DEVICES)
        self._devices.clear()
        for entity in resp["items"]:
            self._devices.append(device.Device(self, entity))

    def _update_device(self, device_id):
        return self._get_request(API_RESOURCE_DEVICE_STATUS.format(device_id=device_id))

    def _get_request(self, resource):
        headers = {"Authorization": "Bearer " + self._token}
        try:
            resp = requests.get(API_BASE + resource, headers=headers)
            if resp.ok:
                return json.loads(resp.content)
        except requests.exceptions.RequestException as exception:
            _LOGGER.warning("Exception: %s", exception)
        return None

    def update(self):
        """Retrieves the latest status for all devices"""
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
        """Gets loaded devices"""
        return self._devices
