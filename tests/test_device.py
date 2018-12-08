"""Tests for the Device file."""

# pylint: disable=missing-docstring

import json
from pysmartthings.smartthings import Device, API
from . import api_mock


class TestDevice:
    """Tests for the Device class."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def test_initialize():
        """Tests whether the Device class initializes correctly."""
        # arrange
        entity = TestDevice._get_device_entity()
        # act
        device = Device(None, entity)
        # assert
        assert device.device_id == "743de49f-036f-4e9c-839a-2f89d57607db"
        assert device.name == "GE In-Wall Smart Dimmer"
        assert device.label == "Front Porch Lights"
        assert device.location_id == "397678e5-9995-4a39-9d9f-ae6ba310236b"
        assert device.type == "DTH"
        assert device.device_type_id == "8a9d4b1e3b9b1fe3013b9b206a7f000d"
        assert device.device_type_name == "Dimmer Switch"
        assert device.device_type_network == "ZWAVE"
        assert device.capabilities == [
            "switch", "switchLevel", "refresh", "indicator",
            "sensor", "actuator", "healthCheck", "light"]

    @staticmethod
    def test_update(requests_mock):
        """Tests updating the status of the device."""
        # arrange
        api_mock.setup(requests_mock)
        device = Device(API(api_mock.API_TOKEN),
                        TestDevice._get_device_entity())
        # act
        device.update()
        # assert
        assert device.status == {"light": "off",
                                 "switchLevel": 46, "switch": "off"}

    @staticmethod
    def _get_device_entity():
        with open("tests/json/device.json", "r") as json_file:
            return json.load(json_file)
