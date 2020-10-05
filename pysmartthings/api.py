"""Utility for invoking the SmartThings Cloud API."""

from typing import Optional, Sequence

from aiohttp import BasicAuth, ClientSession

from .errors import APIInvalidGrant, APIResponseError

API_OAUTH_TOKEN = "https://auth-global.api.smartthings.com/oauth/token"
API_BASE = "https://api.smartthings.com/v1/"
API_LOCATIONS = "locations"
API_LOCATION = API_LOCATIONS + "/{location_id}"
API_ROOMS = "locations/{location_id}/rooms"
API_ROOM = "locations/{location_id}/rooms/{room_id}"
API_DEVICES = "devices"
API_DEVICE = API_DEVICES + "/{device_id}"
API_DEVICE_STATUS = "devices/{device_id}/status"
API_DEVICE_COMMAND = "devices/{device_id}/commands"
API_APPS = "apps"
API_APP = "apps/{app_id}"
API_APP_OAUTH = "apps/{app_id}/oauth"
API_APP_OAUTH_GENERATE = "apps/{app_id}/oauth/generate"
API_APP_SETTINGS = "apps/{app_id}/settings"
API_INSTALLEDAPPS = "installedapps"
API_INSTALLEDAPP = "installedapps/{installed_app_id}"
API_SUBSCRIPTIONS = API_INSTALLEDAPP + "/subscriptions"
API_SUBSCRIPTION = API_SUBSCRIPTIONS + "/{subscription_id}"
API_SCENES = "scenes"
API_SCENE_EXECUTE = "scenes/{scene_id}/execute"


class Api:
    """
    Wrapper around the SmartThings Cloud API operations.

    https://smartthings.developer.samsung.com/docs/api-ref/st-api.html
    """

    __slots__ = ["_session", "_token", "_api_base"]

    def __init__(self, session: ClientSession, token: str, *, api_base: str = API_BASE):
        """Create a new API with the given session and token."""
        self._session = session
        self._token = token
        self._api_base = api_base

    async def get_locations(self) -> dict:
        """
        Get locations.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/listLocations
        """
        return await self.get_items(API_LOCATIONS)

    async def get_location(self, location_id: str) -> dict:
        """
        Get a specific location.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getLocation
        """
        return await self.get(API_LOCATION.format(location_id=location_id))

    async def get_rooms(self, location_id: str) -> dict:
        """
        Get a location's rooms.

        This API call is undocumented.
        """
        return await self.get_items(API_ROOMS.format(location_id=location_id))

    async def get_room(self, location_id: str, room_id: str) -> dict:
        """
        Get a specific room within a location.

        This API call is undocumented.
        """
        return await self.get(API_ROOM.format(location_id=location_id, room_id=room_id))

    async def create_room(self, location_id: str, data: dict):
        """
        Create a room.

        This API call is undocumented.
        """
        return await self.post(API_ROOMS.format(location_id=location_id), data)

    async def update_room(self, location_id: str, room_id: str, data: dict):
        """
        Update a room.

        This API call is undocumented.
        """
        return await self.put(
            API_ROOM.format(location_id=location_id, room_id=room_id), data
        )

    async def delete_room(self, location_id: str, room_id: str):
        """
        Delete a room.

        This API call is undocumented.
        """
        return await self.delete(
            API_ROOM.format(location_id=location_id, room_id=room_id)
        )

    async def get_devices(self, params: Optional = None) -> dict:
        """
        Get the device definitions.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDevices
        """
        return await self.get_items(API_DEVICES, params=params)

    async def get_device(self, device_id: str) -> dict:
        """
        Get as specific device.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDevice
        """
        return await self.get(API_DEVICE.format(device_id=device_id))

    async def get_device_status(self, device_id: str) -> dict:
        """Get the status of a specific device."""
        return await self.get(API_DEVICE_STATUS.format(device_id=device_id))

    async def post_device_command(
        self, device_id, component_id, capability, command, args
    ) -> object:
        """
        Execute commands on a device.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/executeDeviceCommands
        """
        data = {
            "commands": [
                {
                    "component": component_id,
                    "capability": capability,
                    "command": command,
                }
            ]
        }
        if args:
            data["commands"][0]["arguments"] = args

        return await self.post(API_DEVICE_COMMAND.format(device_id=device_id), data)

    async def get_apps(self, params: Optional = None) -> dict:
        """
        Get list of apps.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/listApps
        """
        return await self.get_items(API_APPS, params=params)

    async def get_app(self, app_id: str) -> dict:
        """
        Get the details of the specific app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getApp
        """
        return await self.get(API_APP.format(app_id=app_id))

    async def create_app(self, data: dict) -> dict:
        """
        Create a new app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/createApp
        """
        return await self.post(API_APPS, data)

    async def update_app(self, app_id: str, data: dict) -> dict:
        """
        Update an existing app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/updateApp
        """
        return await self.put(API_APP.format(app_id=app_id), data)

    async def delete_app(self, app_id: str):
        """
        Delete an app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteApp
        """
        return await self.delete(API_APP.format(app_id=app_id))

    async def get_app_settings(self, app_id: str) -> dict:
        """
        Get an app's settings.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getAppSettings
        """
        return await self.get(API_APP_SETTINGS.format(app_id=app_id))

    async def update_app_settings(self, app_id: str, data: dict) -> dict:
        """
        Update an app's settings.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/updateAppSettings
        """
        return await self.put(API_APP_SETTINGS.format(app_id=app_id), data)

    async def get_app_oauth(self, app_id: str) -> dict:
        """
        Get an app's oauth settings.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getAppOauth
        """
        return await self.get(API_APP_OAUTH.format(app_id=app_id))

    async def update_app_oauth(self, app_id: str, data: dict) -> dict:
        """
        Update an app's oauth settings.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/updateAppOauth
        """
        return await self.put(API_APP_OAUTH.format(app_id=app_id), data)

    async def generate_app_oauth(self, app_id: str, data: dict) -> dict:
        """
        Generate a new app oauth client/secret.

         https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/generateAppOauth
        """
        return await self.post(API_APP_OAUTH_GENERATE.format(app_id=app_id), data)

    async def get_installed_apps(self, params: Optional = None) -> dict:
        """
        Get list of installedapps.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/listInstallations
        """
        return await self.get_items(API_INSTALLEDAPPS, params=params)

    async def get_installed_app(self, installed_app_id: str) -> dict:
        """
        Get the details of the specific installedapp.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getInstallation
        """
        return await self.get(
            API_INSTALLEDAPP.format(installed_app_id=installed_app_id)
        )

    async def delete_installed_app(self, installed_app_id: str):
        """
        Delete an app.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/deleteInstallation
        """
        return await self.delete(
            API_INSTALLEDAPP.format(installed_app_id=installed_app_id)
        )

    async def get_subscriptions(self, installed_app_id: str) -> dict:
        """
        Get installedapp's subscriptions.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/listSubscriptions
        """
        return await self.get_items(
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id)
        )

    async def create_subscription(self, installed_app_id: str, data: dict) -> dict:
        """
        Create a subscription for an installedapp.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/saveSubscription
        """
        return await self.post(
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id), data
        )

    async def delete_all_subscriptions(self, installed_app_id: str) -> dict:
        """
        Delete all subscriptions for an installedapp.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteAllSubscriptions
        """
        return await self.delete(
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id)
        )

    async def get_subscription(
        self, installed_app_id: str, subscription_id: str
    ) -> dict:
        """
        Get an individual subscription.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getSubscription
        """
        return await self.get(
            API_SUBSCRIPTION.format(
                installed_app_id=installed_app_id, subscription_id=subscription_id
            )
        )

    async def delete_subscription(self, installed_app_id: str, subscription_id: str):
        """
        Delete an individual subscription.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteSubscription
        """
        return await self.delete(
            API_SUBSCRIPTION.format(
                installed_app_id=installed_app_id, subscription_id=subscription_id
            )
        )

    async def get_scenes(self, params: Optional = None):
        """
        Get scenes.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/listScenes
        """
        return await self.get_items(API_SCENES, params=params)

    async def execute_scene(self, scene_id: str) -> bool:
        """
        Execute a scene.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/executeScene
        """
        return await self.post(API_SCENE_EXECUTE.format(scene_id=scene_id), data=None)

    @property
    def session(self) -> ClientSession:
        """Get the instance of the session."""
        return self._session

    @session.setter
    def session(self, value: ClientSession):
        """Set the instance of the session."""
        self._session = value

    @property
    def token(self):
        """Get the token used when making requests."""
        return self._token

    @token.setter
    def token(self, value):
        """Set the token to use when making requests."""
        self._token = value

    async def request(
        self, method: str, url: str, params: dict = None, data: dict = None
    ):
        """Perform a request against the specified parameters."""
        async with self._session.request(
            method,
            url,
            params=params,
            json=data,
            headers={"Authorization": "Bearer " + self._token},
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status in (400, 422, 429, 500):
                data = None
                try:
                    data = await resp.json()
                except Exception:  # pylint: disable=broad-except
                    pass
                raise APIResponseError(
                    resp.request_info,
                    resp.history,
                    status=resp.status,
                    message=resp.reason,
                    headers=resp.headers,
                    data=data,
                )
            resp.raise_for_status()

    async def get(self, resource: str, *, params: dict = None):
        """Get a resource."""
        return await self.request("get", self._api_base + resource, params)

    async def get_items(self, resource: str, *, params: dict = None):
        """Perform requests for a list of items that may have pages."""
        resp = await self.request("get", self._api_base + resource, params, None)
        items = resp.get("items", [])
        next_link = Api._get_next_link(resp)
        while next_link:
            resp = await self.request("get", next_link, params, None)
            items.extend(resp.get("items", []))
            next_link = Api._get_next_link(resp)
        return items

    async def post(self, resource: str, data: Optional[Sequence]):
        """Perform a post request."""
        return await self.request("post", self._api_base + resource, data=data)

    async def put(self, resource: str, data: Optional[Sequence]):
        """Perform a put request."""
        return await self.request("put", self._api_base + resource, data=data)

    async def delete(self, resource: str, *, params: dict = None):
        """Delete a resource."""
        return await self.request("delete", self._api_base + resource, params)

    async def generate_tokens(
        self, client_id: str, client_secret: str, refresh_token: str
    ):
        """Obtain a new access and refresh token."""
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        async with self._session.request(
            "post",
            API_OAUTH_TOKEN,
            auth=BasicAuth(client_id, client_secret),
            data=payload,
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 400:
                data = {}
                try:
                    data = await resp.json()
                except Exception:  # pylint: disable=broad-except
                    pass
                raise APIInvalidGrant(data.get("error_description"))
            resp.raise_for_status()

    @staticmethod
    def _get_next_link(data):
        links = data.get("_links")
        if not links:
            return None
        next_link = links.get("next")
        if not next_link:
            return None
        return next_link.get("href")
