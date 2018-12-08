"""A Mock API for SmartThings."""

import json
from pysmartthings import api

API_TOKEN = "Test Token"


def setup(requests_mock):
    """Configure request mocks the API calls."""
    # locations
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_LOCATIONS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=__get_json("locations.json"))
    # devices
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_DEVICES,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=__get_json("devices.json"))

    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_DEVICE_STATUS.format(
            device_id="743de49f-036f-4e9c-839a-2f89d57607db"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=__get_json("device_main_status.json"))


def __get_json(file):
    with open("tests/json/" + file, "r") as json_file:
        return json.load(json_file)
