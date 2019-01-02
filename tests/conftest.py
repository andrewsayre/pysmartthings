"""Define test configuration."""
import pytest

from pysmartthings.api import Api, API_BASE, API_LOCATIONS, API_LOCATION
from pysmartthings.smartthings import SmartThings

from .utilities import ClientMocker

AUTH_TOKEN = '9b3fd445-42d6-441b-b386-99ea51e13cb0'
LOCATION_ID = '397678e5-9995-4a39-9d9f-ae6ba310236b'


def register_url_mocks(mocker):
    """Register the URLs we need to mock."""
    mocker.default_headers = {'Authorization': "Bearer " + AUTH_TOKEN}
    mocker.base_url = API_BASE

    # Locations
    mocker.get(API_LOCATIONS, response='locations')
    mocker.get(API_LOCATION.format(location_id=LOCATION_ID),
               response='location')


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
