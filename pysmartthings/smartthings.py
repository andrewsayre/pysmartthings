"""Define the SmartThings Cloud API."""

from typing import List

from .api import API
from .app import App, AppEntity
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

    def devices(self) -> List:
        """Retrieve SmartThings devices."""
        resp = self._api.get_devices()
        return [DeviceEntity(self._api, entity) for entity in resp["items"]]

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
        return self._api.delete_app(app_id) == {}

    def get_app_oauth(self, app_id: str) -> OAuthEntity:
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
