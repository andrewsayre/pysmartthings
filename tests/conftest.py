"""Define test configuration."""
import pytest

from pysmartthings.api import (
    API_BASE, API_DEVICE, API_DEVICE_COMMAND, API_DEVICE_STATUS, API_DEVICES,
    API_LOCATION, API_LOCATIONS, Api)
from pysmartthings.smartthings import SmartThings

from .utilities import ClientMocker

AUTH_TOKEN = '9b3fd445-42d6-441b-b386-99ea51e13cb0'
LOCATION_ID = '397678e5-9995-4a39-9d9f-ae6ba310236b'
DEVICE_ID = '743de49f-036f-4e9c-839a-2f89d57607db'


def register_url_mocks(mocker):
    """Register the URLs we need to mock."""
    mocker.default_headers = {'Authorization': "Bearer " + AUTH_TOKEN}
    mocker.base_url = API_BASE

    # Locations
    mocker.get(API_LOCATIONS, response='locations')
    mocker.get(API_LOCATION.format(location_id=LOCATION_ID),
               response='location')

    # Devices
    mocker.get(API_DEVICES, response='devices')
    mocker.get(API_DEVICES, response='devices_filtered', params=[
        ('locationId', LOCATION_ID),
        ('capability', 'switch'),
        ('deviceId', 'edd26ac6-d156-4505-9647-3b20118ae4d1'),
        ('deviceId', 'be1a61ce-c2a4-4b32-bf8c-31de6d3fa7dd')])
    mocker.get(API_DEVICE.format(device_id=DEVICE_ID), response='device')
    mocker.get(API_DEVICE_STATUS.format(device_id=DEVICE_ID),
               response='device_status')
    mocker.post(API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
                request='device_command_post_switch_on', response={})
    mocker.post(API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
                request='device_command_post_switch_off', response={})
    mocker.post(API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
                request='device_command_post_set_level', response={})


@pytest.fixture
def smartthings(event_loop):
    """Fixture for testing against the SmartThings class."""
    # Python 3.5 doesn't support yield in an async method so we have to
    # run the creation and clean-up of the session in the loop manually.
    mocker = ClientMocker()
    register_url_mocks(mocker)
    session = event_loop.run_until_complete(
        __create_session(event_loop, mocker))
    yield SmartThings(AUTH_TOKEN, session)
    event_loop.run_until_complete(session.close())


@pytest.fixture
def api(event_loop):
    """Fixture for testing against the API."""
    # Python 3.5 doesn't support yield in an async method so we have to
    # run the creation and clean-up of the session in the loop manually.
    mocker = ClientMocker()
    register_url_mocks(mocker)
    session = event_loop.run_until_complete(
        __create_session(event_loop, mocker))
    yield Api(session, AUTH_TOKEN)
    event_loop.run_until_complete(session.close())


async def __create_session(event_loop, mocker):
    return mocker.create_session(event_loop)
