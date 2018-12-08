"""Utility for invoking the SmartThings Cloud API."""

import logging
import requests

API_BASE: str = 'https://api.smartthings.com/v1/'
API_RESOURCE_LOCATIONS = "locations"
API_RESOURCE_DEVICES: str = "devices"
API_RESOURCE_DEVICE_STATUS: str = "devices/{device_id}/components/main/status"
API_RESOURCE_DEVICE_COMMAND: str = "devices/{device_id}/commands"

_LOGGER = logging.getLogger(__name__)


class API:
    """
    Utility for invoking the SmartThings Cloud API.

    https://smartthings.developer.samsung.com/docs/api-ref/st-api.html
    """

    def __init__(self, token):
        """Initialize a new instance of the API class."""
        self._headers = {"Authorization": "Bearer " + token}

    def get_locations(self):
        """
        Get locations.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/listLocations
        """
        return self._get_request(API_RESOURCE_LOCATIONS)

    def get_devices(self):
        """
        Get the device definitions.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDevices
        """
        return self._get_request(API_RESOURCE_DEVICES)

    def get_device_status(self, device_id):
        """Get the status of a specific device."""
        return self._get_request(
            API_RESOURCE_DEVICE_STATUS.format(device_id=device_id))

    def post_command(self, device_id, capability, command, args,
                     component="main"):
        """
        Execute commands on a device.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/executeDeviceCommands
        """
        data = {
            "commands": [
                {
                    "component": component,
                    "capability": capability,
                    "command": command,
                }
            ]
        }
        if args:
            data["commands"][0]["arguments"] = args

        return self._post_request(
            API_RESOURCE_DEVICE_COMMAND.format(device_id=device_id), data)

    def _get_request(self, resource):
        try:
            resp = requests.get(API_BASE + resource, headers=self._headers)
            if resp.content:
                return resp.json()
            return True
        except requests.exceptions.RequestException as exception:
            _LOGGER.warning("Exception: %s", exception)
        return None

    def _post_request(self, resource, data):
        try:
            resp = requests.post(
                API_BASE + resource,
                json=data,
                headers=self._headers)
            if resp.ok:
                if resp.content:
                    return resp.json()
                return True
        except requests.exceptions.RequestException as exception:
            _LOGGER.warning("Exception: %s", exception)
        return None
