import pysmartthings
import json


class Test_Device(object):
    def test_initialize(self):
        with open("tests/json/device.json", "r") as json_file:
            entity = json.load(json_file)

        device = pysmartthings.smartthings.Device(None, entity)

        assert device.device_id == "743de49f-036f-4e9c-839a-2f89d57607db"
