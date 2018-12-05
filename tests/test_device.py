"""Tests for the Device file."""

import json
import pysmartthings


class TestDevice:
    """Tests for the Device class."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def test_initialize():
        """Tests whether the Device class initializes correctly."""
        # arrange
        with open("tests/json/device.json", "r") as json_file:
            entity = json.load(json_file)
        # act
        device = pysmartthings.smartthings.Device(None, entity)
        # assert
        assert device.device_id == "743de49f-036f-4e9c-839a-2f89d57607db"
