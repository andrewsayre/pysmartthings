"""Define the app module."""

import re
from typing import List, Optional

from .api import Api
from .entity import Entity

APP_TYPE_LAMBDA = "LAMBDA_SMART_APP"
APP_TYPE_WEBHOOK = "WEBHOOK_SMART_APP"
CLASSIFICATION_AUTOMATION = "AUTOMATION"

_APP_NAME_PATTERN = re.compile("^[a-z0-9._-]{1,250}$", re.IGNORECASE)


class App:
    """Define the app class."""

    def __init__(self):
        """Initialize a new instance of the App class."""
        self._app_name = None
        self._display_name = None
        self._description = None
        self._single_instance = False
        self._app_type = None
        self._classifications = []
        self._lambda_functions = []
        self._webhook_target_url = None
        self._webhook_public_key = None
        self._app_id = None
        self._created_date = None
        self._last_updated_date = None

    def apply_data(self, data: dict):
        """Set the states of the app with the supplied data."""
        self._app_name = data["appName"]
        self._app_id = data["appId"]
        self._app_type = data["appType"]
        self._classifications = data["classifications"]
        self._display_name = data["displayName"]
        self._description = data["description"]
        self._created_date = data.get("createdDate", self._created_date)
        self._last_updated_date = data.get("lastUpdatedDate", self._last_updated_date)
        self._single_instance = data.get("singleInstance", self._single_instance)
        if self.app_type == APP_TYPE_WEBHOOK and "webhookSmartApp" in data:
            self._webhook_target_url = data["webhookSmartApp"]["targetUrl"]
            self._webhook_public_key = data["webhookSmartApp"]["publicKey"]
        if self.app_type == APP_TYPE_LAMBDA and "lambdaSmartApp" in data:
            self._lambda_functions = data["lambdaSmartApp"]["functions"]

    def to_data(self) -> dict:
        """Get a data structure representing this entity."""
        data = {
            "appName": self._app_name,
            "displayName": self._display_name,
            "description": self._description,
            "singleInstance": self._single_instance,
            "classifications": self._classifications,
            "appType": self._app_type,
        }
        if self._app_type == APP_TYPE_WEBHOOK:
            data["webhookSmartApp"] = {"targetUrl": self._webhook_target_url}
        if self._app_type == APP_TYPE_LAMBDA:
            data["lambdaSmartApp"] = {"functions": self._lambda_functions}
        return data

    @property
    def app_id(self) -> str:
        """Get the application id."""
        return self._app_id

    @property
    def created_date(self):
        """Get the created date of the app."""
        return self._created_date

    @property
    def last_updated_date(self):
        """Get the last updated date of the app."""
        return self._last_updated_date

    @property
    def app_name(self) -> str:
        """
        Get the app name.

        A globally unique, developer-defined identifier for an app. It is
        alpha-numeric, may contain dashes, underscores, periods, and must
        be less then 250 characters long. ^[a-z0-9.-_]{1,250}$
        """
        return self._app_name

    @app_name.setter
    def app_name(self, value: str):
        """Set the app name."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if not _APP_NAME_PATTERN.match(value):
            raise ValueError(
                "value must be alpha-numeric, may contain dashes "
                "underscores, periods, and must be less then 250 "
                "characters long."
            )
        self._app_name = value

    @property
    def display_name(self) -> str:
        """
        Get the display name.

        A default display name for an app. <= 75 characters
        """
        return self._display_name

    @display_name.setter
    def display_name(self, value: str):
        """Set the display name."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if len(value) > 75:
            raise ValueError("value must be <= 75 characters in length.")
        self._display_name = value

    @property
    def description(self) -> str:
        """
        Get the description.

        A default description for an app. <= 250 characters
        """
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the description."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if len(value) > 250:
            raise ValueError("value must be <= 250 characters in length.")
        self._description = value

    @property
    def single_instance(self) -> bool:
        """
        Get the single instance parameter.

        Inform the installation systems that a particular app can only be
        installed once within a user's account.
        """
        return self._single_instance

    @single_instance.setter
    def single_instance(self, value: bool):
        """Set the single instance parameter."""
        self._single_instance = bool(value)

    @property
    def classifications(self) -> List[str]:
        """Get the classifications of the app."""
        return self._classifications

    @classifications.setter
    def classifications(self, value: List[str]):
        """Set the classifications of the app."""
        self._classifications = list(value)

    @property
    def app_type(self) -> str:
        """
        Get the app type.

        Denotes the type of app. "LAMBDA_SMART_APP" "WEBHOOK_SMART_APP"
        """
        return self._app_type

    @app_type.setter
    def app_type(self, value: str):
        """Set the app type."""
        if value not in (APP_TYPE_LAMBDA, APP_TYPE_WEBHOOK):
            raise ValueError(
                "value must be 'LAMBDA_SMART_APP' " "or 'WEBHOOK_SMART_APP'"
            )
        self._app_type = value

    @property
    def lambda_functions(self) -> List[str]:
        """
        Get the list of AWS arns referencing a Lambda function.

        Details related to a Lambda Smart App implementation. This model
        should only be specified for apps of type LAMBDA_SMART_APP.
        """
        return self._lambda_functions

    @property
    def webhook_target_url(self) -> str:
        """Get the URL that should be invoked during execution."""
        return self._webhook_target_url

    @webhook_target_url.setter
    def webhook_target_url(self, value: str):
        """Set the URL that should be invoked during execution."""
        self._webhook_target_url = value

    @property
    def webhook_public_key(self) -> str:
        """Get the public half of an RSA key pair."""
        return self._webhook_public_key


class AppSettings:
    """Define a SmartThings app settings."""

    def __init__(self, app_id: str):
        """Create a new instance of the AppSettings class."""
        self._app_id = app_id
        self._settings = {}

    def apply_data(self, data: dict):
        """Set the states of the app with the supplied data."""
        self._settings = data.get("settings", {})

    def to_data(self) -> dict:
        """Get a data structure representing the entity."""
        return {"settings": self._settings}

    @property
    def app_id(self):
        """Get the associated app id."""
        return self._app_id

    @property
    def settings(self) -> dict:
        """Get the settings for the app."""
        return self._settings

    @settings.setter
    def settings(self, value: dict):
        """Set the settings for the app."""
        self._settings = value


class AppSettingsEntity(Entity, AppSettings):
    """Define a SmartThings App settings entity."""

    def __init__(self, api: Api, app_id: str, data=None):
        """Create a new instance of the AppSettingEntity class."""
        Entity.__init__(self, api)
        AppSettings.__init__(self, app_id)
        if data:
            self.apply_data(data)

    async def refresh(self):
        """Refresh the value of the entity."""
        if not self._app_id:
            raise ValueError("Cannot refresh without an app_id")
        data = await self._api.get_app_settings(self._app_id)
        self.apply_data(data)

    async def save(self):
        """Save the value of the entity."""
        if not self._app_id:
            raise ValueError("Cannot save without an app_id")
        data = await self._api.update_app_settings(self._app_id, self.to_data())
        self.apply_data(data)


class AppOAuth:
    """Define the app OAuth settings."""

    def __init__(self, app_id: str):
        """Initialize a new instance of the OAuth class."""
        self._app_id = app_id
        self._client_name = None
        self._scope = []

    def to_data(self) -> dict:
        """Get a data representation of the instance."""
        return {"clientName": self._client_name, "scope": self._scope}

    def apply_data(self, data: dict):
        """Load the data of the instance."""
        self._client_name = data["clientName"]
        self._scope = data.get("scope", self._scope)

    @property
    def app_id(self) -> str:
        """Get the app id the settings are associated with."""
        return self._app_id

    @property
    def client_name(self) -> str:
        """Get the name given to the OAuth Client."""
        return self._client_name

    @client_name.setter
    def client_name(self, value: str):
        """Set the name given to the OAuth client."""
        if not value:
            raise ValueError("Value can not be None or an empty string.")
        self._client_name = value

    @property
    def scope(self) -> List[str]:
        """Get the list of SmartThings API OAuth scope identifiers."""
        return self._scope


class AppOAuthEntity(Entity, AppOAuth):
    """Define oauth client settings."""

    def __init__(self, api: Api, app_id: str, data=None):
        """Create a new instance of the OAuth class."""
        Entity.__init__(self, api)
        AppOAuth.__init__(self, app_id)
        if data:
            self.apply_data(data)

    async def refresh(self):
        """Retrieve the latest values from the API."""
        data = await self._api.get_app_oauth(self._app_id)
        if data:
            self.apply_data(data)

    async def save(self):
        """Save changes to the app OAuth Client settings."""
        response = await self._api.update_app_oauth(self._app_id, self.to_data())
        if response:
            self.apply_data(response)


class AppEntity(Entity, App):
    """Define a SmartThings App entity."""

    def __init__(self, api: Api, data=None):
        """Create a new instance of the AppEntity class."""
        Entity.__init__(self, api)
        App.__init__(self)
        if data:
            self.apply_data(data)

    async def refresh(self):
        """Refresh the app information using the API."""
        data = await self._api.get_app(self._app_id)
        self.apply_data(data)

    async def save(self):
        """Save the changes made to the app."""
        response = await self._api.update_app(self._app_id, self.to_data())
        self.apply_data(response)

    async def oauth(self) -> AppOAuthEntity:
        """Get the app's OAuth settings."""
        entity = await self._api.get_app_oauth(self._app_id)
        return AppOAuthEntity(self._api, self._app_id, entity)

    async def settings(self) -> AppSettingsEntity:
        """Get the app's settings."""
        entity = await self._api.get_app_settings(self._app_id)
        return AppSettingsEntity(self._api, self._app_id, entity)


class AppOAuthClient:
    """Define an oauth client information."""

    def __init__(self, data: Optional[dict]):
        """Create a new instance of the OAuthClient."""
        self._client_id = None
        self._client_secret = None
        if data:
            self.apply_data(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        self._client_id = data["oauthClientId"]
        self._client_secret = data["oauthClientSecret"]

    @property
    def client_id(self):
        """Get the client id."""
        return self._client_id

    @property
    def client_secret(self):
        """Get the client secret."""
        return self._client_secret


class AppOAuthClientEntity(AppOAuthClient):
    """Define an oauth client information details."""

    def __init__(self, api: Api, app_id: str, data: Optional[dict]):
        """Init the class."""
        self._client_details = AppOAuthEntity(api, app_id, None)
        super().__init__(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        super().apply_data(data)
        self._client_details.apply_data(data["oauthClientDetails"])

    @property
    def client_details(self) -> AppOAuthEntity:
        """Get the OAuth entity."""
        return self._client_details
