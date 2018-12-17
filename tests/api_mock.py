"""A Mock API for SmartThings."""

from pysmartthings import api

from .utilities import get_json

API_TOKEN = "Test Token"


def setup(requests_mock):
    """Configure request mocks the API calls."""
    # GET location/
    requests_mock.get(
        api.API_BASE + api.API_LOCATIONS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("locations.json"))

    # GET devices/
    requests_mock.get(
        api.API_BASE + api.API_DEVICES,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("devices.json"))

    # GET device/{guid}/
    requests_mock.get(
        api.API_BASE + api.API_DEVICE_STATUS.format(
            device_id="743de49f-036f-4e9c-839a-2f89d57607db"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("device_main_status.json"))

    # GET app/
    requests_mock.get(
        api.API_BASE + api.API_APPS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("apps.json"))

    # GET app/{guid}
    requests_mock.get(
        api.API_BASE + api.API_APP.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_get.json"))

    # POST app/{guid}
    requests_mock.post(
        api.API_BASE + api.API_APPS,
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_post_response.json"),
        additional_matcher=__app_post_matcher)

    # PUT app/{guid}
    requests_mock.put(
        api.API_BASE + api.API_APP.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_put_response.json"),
        additional_matcher=__app_put_matcher)

    # DELETE app/{guid}
    requests_mock.delete(
        api.API_BASE + api.API_APP.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json={})

    # GET app/{guid}/oauth
    requests_mock.get(
        api.API_BASE + api.API_APP_OAUTH.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_oauth_get_response.json"))

    # PUT app/{guid}/oauth
    requests_mock.put(
        api.API_BASE + api.API_APP_OAUTH.format(
            app_id="c6cde2b0-203e-44cf-a510-3b3ed4706996"),
        headers={"Authorization": "Bearer " + API_TOKEN},
        json=get_json("app_oauth_put_response.json"),
        additional_matcher=__app_oauth_put_matcher)


def __app_put_matcher(request) -> bool:
    return get_json('app_put_request.json') == request.json()


def __app_post_matcher(request) -> bool:
    return get_json('app_post_request.json') == request.json()


def __app_oauth_put_matcher(request) -> bool:
    return get_json('app_oauth_put_request.json') == request.json()
