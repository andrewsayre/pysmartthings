"""A Mock API for SmartThings."""

from collections import namedtuple

from requests import Request, Response
from requests_mock.response import create_response

from pysmartthings import api, oauthapi

from .utilities import get_json

API_TOKEN = "Test Token"
APP_ID = 'c6cde2b0-203e-44cf-a510-3b3ed4706996'
DEVICE_ID = '743de49f-036f-4e9c-839a-2f89d57607db'
INSTALLED_APP_ID = '4514eb36-f5fd-4ab2-9520-0597acd1d212'
SUBSCRIPTION_ID = '7bdf5909-57c4-41f3-9089-e520513bd92a'
LOCATION_ID = '397678e5-9995-4a39-9d9f-ae6ba310236b'
CLIENT_ID = '7cd4d474-7b36-4e03-bbdb-4cd4ae45a2be'
CLIENT_SECRET = '9b3fd445-42d6-441b-b386-99ea51e13cb0'
REFRESH_TOKEN = 'a86a5c8e-0014-44a6-8980-5846633972dd'

UrlMock = namedtuple('UrlMock', 'method url request response')

URLS = [
    UrlMock('GET', api.API_LOCATIONS, None, 'locations.json'),
    UrlMock('GET', api.API_LOCATION.format(location_id=LOCATION_ID),
            None, 'location.json'),
    UrlMock('GET', api.API_DEVICES, None, 'devices.json'),
    UrlMock('GET', api.API_DEVICES +
            "?locationId=397678e5-9995-4a39-9d9f-ae6ba310236b" +
            "&capability=switch" +
            "&deviceId=edd26ac6-d156-4505-9647-3b20118ae4d1" +
            "&deviceId=be1a61ce-c2a4-4b32-bf8c-31de6d3fa7dd",
            None, 'devices_filtered.json'),
    UrlMock('GET', api.API_DEVICE.format(device_id=DEVICE_ID),
            None, 'device.json'),
    UrlMock('GET', api.API_DEVICE_STATUS.format(device_id=DEVICE_ID),
            None, 'device_status.json'),
    UrlMock('POST', api.API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
            'device_command_post_switch_on.json', {}),
    UrlMock('POST', api.API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
            'device_command_post_switch_off.json', {}),
    UrlMock('POST', api.API_DEVICE_COMMAND.format(device_id=DEVICE_ID),
            'device_command_post_set_level.json', {}),
    UrlMock('GET', api.API_APPS, None, 'apps.json'),
    UrlMock('GET', api.API_APP.format(app_id=APP_ID),
            None, 'app_get.json'),
    UrlMock('POST', api.API_APPS,
            'app_post_request.json', 'app_post_response.json'),
    UrlMock('PUT', api.API_APP.format(app_id=APP_ID),
            'app_put_request.json', 'app_put_response.json'),
    UrlMock('DELETE', api.API_APP.format(app_id=APP_ID), None, {}),
    UrlMock('GET', api.API_APP_SETTINGS.format(app_id=APP_ID),
            None, 'app_settings.json'),
    UrlMock('PUT', api.API_APP_SETTINGS.format(app_id=APP_ID),
            'app_settings.json', 'app_settings.json'),
    UrlMock('GET', api.API_APP_OAUTH.format(app_id=APP_ID),
            None, 'app_oauth_get_response.json'),
    UrlMock('PUT', api.API_APP_OAUTH.format(app_id=APP_ID),
            'app_oauth_put_request.json', 'app_oauth_put_response.json'),
    # InstalledApps
    UrlMock('GET', api.API_INSTALLEDAPPS, None,
            'installedapps_get_response.json'),
    UrlMock('GET', "https://api.smartthings.com/installedapps?"
                   "currentLocationId=NWMwM2U1MTgtMTE4YS00NGNiLTg1YWQtNzg3N2Qw"
                   "YjMwMmU0&currentOffset=MA", None,
            'installedapps_get_response_2.json'),
    UrlMock('GET', api.API_INSTALLEDAPP.format(
        installed_app_id=INSTALLED_APP_ID),
            None, 'installedapp_get_response.json'),
    UrlMock('DELETE', api.API_INSTALLEDAPP.format(
        installed_app_id=INSTALLED_APP_ID), None, {"count": 1}),
    UrlMock('GET', api.API_SUBSCRIPTIONS.format(
        installed_app_id=INSTALLED_APP_ID), None,
            'subscriptions_get_response.json'),
    UrlMock('DELETE', api.API_SUBSCRIPTIONS.format(
        installed_app_id=INSTALLED_APP_ID), None,
            {'count': 3}),
    UrlMock('POST', api.API_SUBSCRIPTIONS.format(
        installed_app_id=INSTALLED_APP_ID),
            'subscription_post_request.json',
            'subscription_post_response.json'),
    UrlMock('GET', api.API_SUBSCRIPTION.format(
        installed_app_id=INSTALLED_APP_ID,
        subscription_id='7bdf5909-57c4-41f3-9089-e520513bd92a'), None,
            'subscription_capability_get_response.json'),
    UrlMock('GET', api.API_SUBSCRIPTION.format(
        installed_app_id=INSTALLED_APP_ID,
        subscription_id='498752fd-db87-4a5e-95f5-25a0e412838d'), None,
            'subscription_device_get_response.json'),
    UrlMock('DELETE', api.API_SUBSCRIPTION.format(
        installed_app_id=INSTALLED_APP_ID,
        subscription_id=SUBSCRIPTION_ID), None,
            {'count': 1})
]


def setup(requests_mock):
    """Configure request mocks the API calls."""
    requests_mock.add_matcher(__matcher)

    requests_mock.register_uri(
        'POST', oauthapi.AUTH_API_TOKEN,
        json=get_json('token_response.json'))


def __matcher(req: Request) -> Response:
    """Match against our registry."""
    match = next((obj for obj in URLS if __match_request(req, obj)), None)
    if match:
        return create_response(req, json=__get_body(match.response))


def __match_request(req: Request, mock: UrlMock):
    """Match the request against the mock setup."""
    if not req.headers.get('Authorization', '') == "Bearer " + API_TOKEN:
        return False
    if not req.method == mock.method:
        return False
    target_url = mock.url if mock.url.startswith('http') \
        else api.API_BASE + mock.url
    if not req.url == target_url:
        return False
    if mock.request and not req.json() == __get_body(mock.request):
        return False
    return True


def __get_body(body):
    if isinstance(body, (dict, list)):
        return body
    if isinstance(body, str):
        return get_json(body)
    return None
