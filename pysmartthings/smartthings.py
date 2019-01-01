"""Define the SmartThings Cloud API."""

from collections import OrderedDict
from typing import List, Optional, Sequence

from .api import API
from .app import App, AppEntity, AppSettings, AppSettingsEntity
from .device import DeviceEntity
from .installedapp import InstalledAppEntity
from .location import LocationEntity
from .oauth import OAuth, OAuthClient, OAuthEntity
from .subscription import Subscription, SubscriptionEntity


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
        return [LocationEntity(self._api, entity) for entity in resp["items"]]

    def location(self, location_id: str) -> LocationEntity:
        """Retrieve a location with the specified ID."""
        entity = self._api.get_location(location_id)
        return LocationEntity(self._api, entity)

    def devices(self, location_ids: Optional[Sequence[str]] = None,
                capabilities: Optional[Sequence[str]] = None,
                device_ids: Optional[Sequence[str]] = None) -> List:
        """Retrieve SmartThings devices."""
        params = OrderedDict()
        if location_ids:
            params['locationId'] = location_ids
        if capabilities:
            params['capability'] = capabilities
        if device_ids:
            params['deviceId'] = device_ids
        resp = self._api.get_devices(params)
        return [DeviceEntity(self._api, entity) for entity in resp["items"]]

    def device(self, device_id: str) -> DeviceEntity:
        """Retrieve a device with the specified ID."""
        entity = self._api.get_device(device_id)
        return DeviceEntity(self._api, entity)

    def apps(self) -> List[AppEntity]:
        """Retrieve list of apps."""
        resp = self._api.get_apps()
        return [AppEntity(self._api, entity) for entity in resp["items"]]

    def app(self, app_id: str) -> AppEntity:
        """Retrieve an app with the specified ID."""
        entity = self._api.get_app(app_id)
        return AppEntity(self._api, entity)

    def create_app(self, app: App) -> (AppEntity, OAuthClient):
        """Create a new app."""
        entity = self._api.create_app(app.to_data())
        return AppEntity(self._api, entity['app']), OAuthClient(entity)

    def delete_app(self, app_id: str):
        """Delete an app."""
        return self._api.delete_app(app_id) == {}

    def app_settings(self, app_id: str) -> AppSettingsEntity:
        """Get an app's settings."""
        return AppSettingsEntity(
            self._api, app_id, self._api.get_app_settings(app_id))

    def update_app_settings(self, data: AppSettings) -> AppSettingsEntity:
        """Update an app's settings."""
        entity = self._api.update_app_settings(data.app_id, data.to_data())
        return AppSettingsEntity(self._api, data.app_id, entity)

    def app_oauth(self, app_id: str) -> OAuthEntity:
        """Get an app's OAuth settings."""
        return OAuthEntity(self._api, app_id, self._api.get_app_oauth(app_id))

    def update_app_oauth(self, data: OAuth) -> OAuthEntity:
        """Update an app's OAuth settings without having to retrieve it."""
        entity = self._api.update_app_oauth(data.app_id, data.to_data())
        return OAuthEntity(self._api, data.app_id, entity)

    def installedapps(self) -> List[InstalledAppEntity]:
        """Get a list of the installed applications."""
        resp = self._api.get_installedapps()
        return [InstalledAppEntity(self._api, entity)
                for entity in resp["items"]]

    def installedapp(self, installed_app_id: str) -> InstalledAppEntity:
        """Get an installedapp with the specified ID."""
        entity = self._api.get_installedapp(installed_app_id)
        return InstalledAppEntity(self._api, entity)

    def delete_installedapp(self, installed_app_id: str):
        """Delete an installedapp."""
        return self._api.delete_installedapp(installed_app_id) == {'count': 1}

    def subscriptions(self, installed_app_id: str) \
            -> List[SubscriptionEntity]:
        """Get an installedapp's subscriptions."""
        resp = self._api.get_subscriptions(installed_app_id)
        return [SubscriptionEntity(self._api, entity)
                for entity in resp["items"]]

    def delete_subscriptions(self, installed_app_id: str) -> int:
        """Delete an installedapp's subscriptions."""
        resp = self._api.delete_all_subscriptions(installed_app_id)
        return resp['count']

    def delete_subscription(self, installed_app_id: str,
                            subscription_id: str):
        """Delete an individual subscription."""
        return self._api.delete_subscription(
            installed_app_id, subscription_id) == {'count': 1}

    def create_subscription(self, subscription: Subscription) \
            -> SubscriptionEntity:
        """Create a new subscription for an installedapp."""
        entity = self._api.create_subscription(
            subscription.installed_app_id, subscription.to_data())
        return SubscriptionEntity(self._api, entity)
