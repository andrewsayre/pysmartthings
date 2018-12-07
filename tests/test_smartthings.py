"""Tests for the SmartThings file."""

import json
from pysmartthings.smartthings import SmartThings
from pysmartthings.api import API_BASE, API_RESOURCE_DEVICES

API_TOKEN = "TEST_TOKEN"


class TestSmartThings:
    """Tests for the SmartThings class."""

    @staticmethod
    def test_devices(requests_mock):
        """Tests whether devices are populated correctly from the API."""

        # arrange
        with open("tests/json/devices.json", "r") as json_file:
            body = json.load(json_file)
        requests_mock.get(
            API_BASE + API_RESOURCE_DEVICES,
            headers={"Authorization": "Bearer " + API_TOKEN},
            json=body)

        # act
        smartthings = SmartThings(API_TOKEN)

        # assert
        assert len(smartthings.devices) == 4
