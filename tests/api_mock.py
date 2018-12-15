"""A Mock API for SmartThings."""

from pysmartthings import api

from .utilities import get_json

API_TOKEN = "Test Token"


def setup(requests_mock):
    """Configure request mocks the API calls."""
    # location/
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_LOCATIONS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("locations.json"))
    # devices/
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_DEVICES,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("devices.json"))
    # device/{guid}/
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_DEVICE_STATUS.format(
            device_id="743de49f-036f-4e9c-839a-2f89d57607db"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("device_main_status.json"))
    # app/
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_APPS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("apps.json"))
    # app/{guid}
    requests_mock.get(
        api.API_BASE + api.API_RESOURCE_APP_DETAILS.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_get.json"))
