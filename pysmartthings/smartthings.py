"""Define the SmartThings Cloud API."""

from typing import List

from .api import API
from .app import App, AppEntity
from .device import Device
from .location import Location
from .oauth import OAuth, OAuthClient, OAuthEntity


class SmartThings:
    """Define a class for interacting with the SmartThings Cloud API."""

    def __init__(self, token):
        """
        Initialize the API.

        :param token: The personal access token used to authenticate to the API
        :type token: str
        """
        self._api = API(token)

    def locations(self) -> List:
        """Retrieve SmartThings locations."""
        resp = self._api.get_locations()
        return [Location(self._api, entity) for entity in resp["items"]]

    def devices(self) -> List:
        """Retrieve SmartThings devices."""
        resp = self._api.get_devices()
        return [Device(self._api, entity) for entity in resp["items"]]

    def apps(self) -> List[AppEntity]:
        """Retrieve list of apps."""
        resp = self._api.get_apps()
        return [AppEntity(self._api, entity) for entity in resp["items"]]

    def create_app(self, app: App) -> (AppEntity, OAuthClient):
        """Create a new app."""
        entity = self._api.create_app(app.to_data())
        return AppEntity(self._api, entity['app']), OAuthClient(entity)

    def delete_app(self, app_id: str):
        """Delete an app."""
        return self._api.delete_app(app_id)

    def get_app_oauth(self, app_id: str) -> OAuthEntity:
        """Get an app's OAuth settings."""
        return OAuthEntity(self._api, app_id, self._api.get_app_oauth(app_id))

    def update_app_oauth(self, data: OAuth) -> OAuthEntity:
        """Update an app's OAuth settings without having to retrieve it."""
        entity = self._api.update_app_oauth(data.app_id, data.to_data())
        return OAuthEntity(self._api, data.app_id, entity)
