"""Define test configuration."""
import glob
import re

from pysmartthings.api import (
    API_APP,
    API_APP_OAUTH,
    API_APP_OAUTH_GENERATE,
    API_APP_SETTINGS,
    API_APPS,
    API_BASE,
    API_DEVICE,
    API_DEVICE_COMMAND,
    API_DEVICE_STATUS,
    API_DEVICES,
    API_INSTALLEDAPP,
    API_INSTALLEDAPPS,
    API_LOCATION,
    API_LOCATIONS,
    API_OAUTH_TOKEN,
    API_ROOM,
    API_ROOMS,
    API_SCENE_EXECUTE,
    API_SCENES,
    API_SUBSCRIPTION,
    API_SUBSCRIPTIONS,
    Api,
)
from pysmartthings.smartthings import SmartThings
import pytest

from .utilities import ClientMocker

APP_ID = "c6cde2b0-203e-44cf-a510-3b3ed4706996"
AUTH_TOKEN = "9b3fd445-42d6-441b-b386-99ea51e13cb0"
CLIENT_ID = "7cd4d474-7b36-4e03-bbdb-4cd4ae45a2be"
CLIENT_SECRET = "9b3fd445-42d6-441b-b386-99ea51e13cb0"
DEVICE_ID = "743de49f-036f-4e9c-839a-2f89d57607db"
INSTALLED_APP_ID = "4514eb36-f5fd-4ab2-9520-0597acd1d212"
LOCATION_ID = "397678e5-9995-4a39-9d9f-ae6ba310236b"
ROOM_ID = "7715151d-0314-457a-a82c-5ce48900e065"
REFRESH_TOKEN = "a86a5c8e-0014-44a6-8980-5846633972dd"
SUBSCRIPTION_ID = "7bdf5909-57c4-41f3-9089-e520513bd92a"
SCENE_ID = "9b58411f-5d26-418d-b193-3434a77c484a"

DEVICE_COMMAND_PATTERN = re.compile(r"(device_command_post_[a-z_]+)")


def register_device_commands(mocker):
    """Register all device commands."""
    files = glob.glob("tests/json/device_command_post_*.json")
    for file in files:
        match = DEVICE_COMMAND_PATTERN.search(file)
        if match:
            mocker.post(
                API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
                request=match.group(),
                response={},
            )


def register_url_mocks(mocker):
    """Register the URLs we need to mock."""
    mocker.default_headers = {"Authorization": "Bearer " + AUTH_TOKEN}
    mocker.base_url = API_BASE

    # Locations
    mocker.get(API_LOCATIONS, response="locations")
    mocker.get(API_LOCATION.format(location_id=LOCATION_ID), response="location")

    # Rooms
    mocker.get(API_ROOMS.format(location_id=LOCATION_ID), response="rooms")
    mocker.get(
        API_ROOM.format(location_id=LOCATION_ID, room_id=ROOM_ID), response="room"
    )
    mocker.post(
        API_ROOMS.format(location_id=LOCATION_ID), request="room_post", response="room"
    )
    mocker.put(
        API_ROOM.format(location_id=LOCATION_ID, room_id=ROOM_ID),
        request="room_put",
        response="room",
    )
    mocker.delete(
        API_ROOM.format(location_id=LOCATION_ID, room_id=ROOM_ID), response={}
    )

    # Devices
    mocker.get(API_DEVICES, response="devices")
    mocker.get(
        API_DEVICES,
        response="devices_filtered",
        params=[
            ("locationId", LOCATION_ID),
            ("capability", "switch"),
            ("deviceId", "edd26ac6-d156-4505-9647-3b20118ae4d1"),
            ("deviceId", "be1a61ce-c2a4-4b32-bf8c-31de6d3fa7dd"),
        ],
    )
    mocker.get(API_DEVICE.format(device_id=DEVICE_ID), response="device")
    mocker.get(API_DEVICE_STATUS.format(device_id=DEVICE_ID), response="device_status")

    # Device Commands
    register_device_commands(mocker)

    # Apps
    mocker.get(API_APPS, response="apps")
    mocker.get(API_APP.format(app_id=APP_ID), response="app_get")
    mocker.post(API_APPS, request="app_post_request", response="app_post_response")
    mocker.put(
        API_APP.format(app_id=APP_ID),
        request="app_put_request",
        response="app_put_response",
    )
    mocker.delete(API_APP.format(app_id=APP_ID), response={})
    mocker.get(API_APP_SETTINGS.format(app_id=APP_ID), response="app_settings")
    mocker.put(
        API_APP_SETTINGS.format(app_id=APP_ID),
        request="app_settings",
        response="app_settings",
    )
    mocker.get(API_APP_OAUTH.format(app_id=APP_ID), response="app_oauth_get_response")
    mocker.put(
        API_APP_OAUTH.format(app_id=APP_ID),
        request="app_oauth_put_request",
        response="app_oauth_put_response",
    )
    mocker.post(
        API_APP_OAUTH_GENERATE.format(app_id=APP_ID),
        request="app_oauth_generate_request",
        response="app_oauth_generate_response",
    )

    # InstalledApps
    mocker.get(API_INSTALLEDAPPS, response="installedapps_get_response")
    mocker.request(
        "get",
        "https://api.smartthings.com/installedapps?"
        "currentLocationId=NWMwM2U1MTgtMTE4YS00NGNiLTg1YWQtNzg3N2Qw"
        "YjMwMmU0&currentOffset=MA",
        headers=mocker.default_headers,
        response="installedapps_get_response_2",
    )
    mocker.get(
        API_INSTALLEDAPP.format(installed_app_id=INSTALLED_APP_ID),
        response="installedapp_get_response",
    )
    mocker.delete(
        API_INSTALLEDAPP.format(installed_app_id=INSTALLED_APP_ID),
        response={"count": 1},
    )

    # InstallApp Subscriptions
    mocker.get(
        API_SUBSCRIPTIONS.format(installed_app_id=INSTALLED_APP_ID),
        response="subscriptions_get_response",
    )
    mocker.delete(
        API_SUBSCRIPTIONS.format(installed_app_id=INSTALLED_APP_ID),
        response={"count": 3},
    )
    mocker.post(
        API_SUBSCRIPTIONS.format(installed_app_id=INSTALLED_APP_ID),
        request="subscription_post_request",
        response="subscription_post_response",
    )
    mocker.get(
        API_SUBSCRIPTION.format(
            installed_app_id=INSTALLED_APP_ID, subscription_id=SUBSCRIPTION_ID
        ),
        response="subscription_capability_get_response",
    )
    mocker.get(
        API_SUBSCRIPTION.format(
            installed_app_id=INSTALLED_APP_ID,
            subscription_id="498752fd-db87-4a5e-95f5-25a0e412838d",
        ),
        response="subscription_device_get_response",
    )
    mocker.delete(
        API_SUBSCRIPTION.format(
            installed_app_id=INSTALLED_APP_ID, subscription_id=SUBSCRIPTION_ID
        ),
        response={"count": 1},
    )

    # OAuth Token
    mocker.request("post", API_OAUTH_TOKEN, response="token_response")

    # Scenes
    mocker.get(API_SCENES, response="scenes")
    mocker.get(
        API_SCENES,
        response="scenes_location_filter",
        params=[("locationId", LOCATION_ID)],
    )
    mocker.post(
        API_SCENE_EXECUTE.format(scene_id=SCENE_ID), response={"status": "success"}
    )


@pytest.fixture
def smartthings(event_loop):
    """Fixture for testing against the SmartThings class."""
    # Python 3.5 doesn't support yield in an async method so we have to
    # run the creation and clean-up of the session in the loop manually.
    mocker = ClientMocker()
    register_url_mocks(mocker)
    session = event_loop.run_until_complete(__create_session(event_loop, mocker))
    yield SmartThings(session, AUTH_TOKEN)
    event_loop.run_until_complete(session.close())


@pytest.fixture
def api(event_loop):
    """Fixture for testing against the API."""
    # Python 3.5 doesn't support yield in an async method so we have to
    # run the creation and clean-up of the session in the loop manually.
    mocker = ClientMocker()
    register_url_mocks(mocker)
    session = event_loop.run_until_complete(__create_session(event_loop, mocker))
    yield Api(session, AUTH_TOKEN)
    event_loop.run_until_complete(session.close())


async def __create_session(event_loop, mocker):
    return mocker.create_session(event_loop)
