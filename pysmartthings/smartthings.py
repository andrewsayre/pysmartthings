"""Define the SmartThings Cloud API."""

from typing import List, Optional, Sequence

from aiohttp import ClientSession

from .api import Api
from .app import (
    App,
    AppEntity,
    AppOAuth,
    AppOAuthClient,
    AppOAuthClientEntity,
    AppOAuthEntity,
    AppSettings,
    AppSettingsEntity,
)
from .device import DeviceEntity
from .installedapp import InstalledAppEntity, InstalledAppStatus
from .location import LocationEntity
from .oauthtoken import OAuthToken
from .room import Room, RoomEntity
from .scene import SceneEntity
from .subscription import Subscription, SubscriptionEntity


class SmartThings:
    """Define a class for interacting with the SmartThings Cloud API."""

    __slots__ = ["_service"]

    def __init__(self, session: ClientSession, token: str):
        """Initialize the SmartThingsApi."""
        self._service = Api(session, token)

    async def locations(self) -> List[LocationEntity]:
        """Retrieve SmartThings locations."""
        resp = await self._service.get_locations()
        return [LocationEntity(self._service, entity) for entity in resp]

    async def location(self, location_id: str) -> LocationEntity:
        """Retrieve a location with the specified ID."""
        entity = await self._service.get_location(location_id)
        return LocationEntity(self._service, entity)

    async def rooms(self, location_id: str) -> List[RoomEntity]:
        """Retrieve a list of rooms for a location."""
        resp = await self._service.get_rooms(location_id)
        return [RoomEntity(self._service, entity) for entity in resp]

    async def room(self, location_id: str, room_id: str) -> RoomEntity:
        """Retrieve a specific room."""
        entity = await self._service.get_room(location_id, room_id)
        return RoomEntity(self._service, entity)

    async def create_room(self, room: Room) -> RoomEntity:
        """Create a room."""
        entity = await self._service.create_room(room.location_id, room.to_data())
        return RoomEntity(self._service, entity)

    async def update_room(self, room: Room) -> RoomEntity:
        """Update a room."""
        entity = await self._service.update_room(
            room.location_id, room.room_id, room.to_data()
        )
        return RoomEntity(self._service, entity)

    async def delete_room(self, location_id: str, room_id: str):
        """Delete a room."""
        return await self._service.delete_room(location_id, room_id) == {}

    async def devices(
        self,
        *,
        location_ids: Optional[Sequence[str]] = None,
        capabilities: Optional[Sequence[str]] = None,
        device_ids: Optional[Sequence[str]] = None
    ) -> List:
        """Retrieve SmartThings devices."""
        params = []
        if location_ids:
            params.extend([("locationId", lid) for lid in location_ids])
        if capabilities:
            params.extend([("capability", cap) for cap in capabilities])
        if device_ids:
            params.extend([("deviceId", did) for did in device_ids])
        resp = await self._service.get_devices(params)
        return [DeviceEntity(self._service, entity) for entity in resp]

    async def device(self, device_id: str) -> DeviceEntity:
        """Retrieve a device with the specified ID."""
        entity = await self._service.get_device(device_id)
        return DeviceEntity(self._service, entity)

    async def apps(self, *, app_type: Optional[str] = None) -> List[AppEntity]:
        """Retrieve list of apps."""
        params = []
        if app_type:
            params.append(("appType", app_type))
        resp = await self._service.get_apps(params)
        return [AppEntity(self._service, entity) for entity in resp]

    async def app(self, app_id: str) -> AppEntity:
        """Retrieve an app with the specified ID."""
        entity = await self._service.get_app(app_id)
        return AppEntity(self._service, entity)

    async def create_app(self, app: App) -> (AppEntity, AppOAuthClient):
        """Create a new app."""
        entity = await self._service.create_app(app.to_data())
        return AppEntity(self._service, entity["app"]), AppOAuthClient(entity)

    async def delete_app(self, app_id: str):
        """Delete an app."""
        return await self._service.delete_app(app_id) == {}

    async def app_settings(self, app_id: str) -> AppSettingsEntity:
        """Get an app's settings."""
        settings = await self._service.get_app_settings(app_id)
        return AppSettingsEntity(self._service, app_id, settings)

    async def update_app_settings(self, data: AppSettings) -> AppSettingsEntity:
        """Update an app's settings."""
        entity = await self._service.update_app_settings(data.app_id, data.to_data())
        return AppSettingsEntity(self._service, data.app_id, entity)

    async def app_oauth(self, app_id: str) -> AppOAuthEntity:
        """Get an app's OAuth settings."""
        oauth = await self._service.get_app_oauth(app_id)
        return AppOAuthEntity(self._service, app_id, oauth)

    async def update_app_oauth(self, data: AppOAuth) -> AppOAuthEntity:
        """Update an app's OAuth settings without having to retrieve it."""
        entity = await self._service.update_app_oauth(data.app_id, data.to_data())
        return AppOAuthEntity(self._service, data.app_id, entity)

    async def generate_app_oauth(self, data: AppOAuth) -> AppOAuthClientEntity:
        """Generate a new oauth client id and secret."""
        entity = await self._service.generate_app_oauth(data.app_id, data.to_data())
        return AppOAuthClientEntity(self._service, data.app_id, entity)

    async def installed_apps(
        self,
        *,
        location_id: Optional[str] = None,
        installed_app_status: Optional[InstalledAppStatus] = None
    ) -> List[InstalledAppEntity]:
        """Get a list of the installed applications."""
        params = []
        if location_id:
            params.append(("locationId", location_id))
        if installed_app_status:
            params.append(("installedAppStatus", installed_app_status.value))
        resp = await self._service.get_installed_apps(params)
        return [InstalledAppEntity(self._service, entity) for entity in resp]

    async def installed_app(self, installed_app_id: str) -> InstalledAppEntity:
        """Get an installedapp with the specified ID."""
        entity = await self._service.get_installed_app(installed_app_id)
        return InstalledAppEntity(self._service, entity)

    async def delete_installed_app(self, installed_app_id: str):
        """Delete an installedapp."""
        result = await self._service.delete_installed_app(installed_app_id)
        return result == {"count": 1}

    async def subscriptions(self, installed_app_id: str) -> List[SubscriptionEntity]:
        """Get an installedapp's subscriptions."""
        resp = await self._service.get_subscriptions(installed_app_id)
        return [SubscriptionEntity(self._service, entity) for entity in resp]

    async def delete_subscriptions(self, installed_app_id: str) -> int:
        """Delete an installedapp's subscriptions."""
        resp = await self._service.delete_all_subscriptions(installed_app_id)
        return resp["count"]

    async def delete_subscription(self, installed_app_id: str, subscription_id: str):
        """Delete an individual subscription."""
        return await self._service.delete_subscription(
            installed_app_id, subscription_id
        ) == {"count": 1}

    async def create_subscription(
        self, subscription: Subscription
    ) -> SubscriptionEntity:
        """Create a new subscription for an installedapp."""
        entity = await self._service.create_subscription(
            subscription.installed_app_id, subscription.to_data()
        )
        return SubscriptionEntity(self._service, entity)

    async def scenes(self, *, location_id: Optional[str] = None):
        """Get a list of scenes and optionally filter by location."""
        params = []
        if location_id:
            params.append(("locationId", location_id))
        resp = await self._service.get_scenes(params)
        return [SceneEntity(self._service, entity) for entity in resp]

    async def execute_scene(self, scene_id: str) -> bool:
        """Execute the scene with the specified id."""
        result = await self._service.execute_scene(scene_id)
        return result == {"status": "success"}

    async def generate_tokens(
        self, client_id: str, client_secret: str, refresh_token: str
    ) -> OAuthToken:
        """Generate a new refresh/access token pair."""
        result = await self._service.generate_tokens(
            client_id, client_secret, refresh_token
        )
        return OAuthToken(self._service, result)
