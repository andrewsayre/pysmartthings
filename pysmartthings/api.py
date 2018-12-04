"""Utility for invoking the SmartThings Cloud API"""

import logging
import requests

API_BASE: str = 'https://api.smartthings.com/v1/'
API_RESOURCE_DEVICES: str = "devices"
API_RESOURCE_DEVICE_STATUS: str = "devices/{device_id}/components/main/status"

_LOGGER = logging.getLogger(__name__)


class API:
    """Utility for invoking the SmartThings Cloud API"""
    def __init__(self, token):
        self._token = token

    def get_devices(self):
        """Gets the device definitions"""
        return self._get_request(API_RESOURCE_DEVICES)

    def get_device_status(self, device_id):
        """Gets the status of a specific device"""
        return self._get_request(API_RESOURCE_DEVICE_STATUS.format(device_id=device_id))

    def _get_request(self, resource):
        headers = {"Authorization": "Bearer " + self._token}
        try:
            resp = requests.get(API_BASE + resource, headers=headers)
            if resp.ok:
                return resp.json()
        except requests.exceptions.RequestException as exception:
            _LOGGER.warning("Exception: %s", exception)
        return None
