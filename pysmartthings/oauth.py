"""Define the oauth module."""

from typing import List, Optional

from .api import API
from .entity import Entity
from .oauthapi import OAuthAPI


class OAuth:
    """Define the app OAuth settings."""

    _app_id: str
    _client_name: str
    _scope: List[str]

    def __init__(self, app_id: str):
        """Initialize a new instance of the OAuth class."""
        self._app_id = app_id
        self._client_name = None
        self._scope = []

    def to_data(self) -> dict:
        """Get a data representation of the instance."""
        return {
            'clientName': self._client_name,
            'scope': self._scope
        }

    def apply_data(self, data: dict):
        """Load the data of the instance."""
        self._client_name = data['clientName']
        self._scope = data.get('scope', self._scope)

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
    def scope(self):
        """Get the ;ist of SmartThings API OAuth scope identifiers."""
        return self._scope


class OAuthEntity(Entity, OAuth):
    """Define oauth client settings."""

    def __init__(self, api: API, app_id: str, data=None):
        """Create a new instance of the OAuth class."""
        Entity.__init__(self, api)
        OAuth.__init__(self, app_id)
        if data:
            self.apply_data(data)

    def refresh(self):
        """Retrieve the latest values from the API."""
        data = self._api.get_app_oauth(self._app_id)
        if data:
            self.apply_data(data)

    def save(self):
        """Save changes to the app OAuth Client settings."""
        response = self._api.update_app_oauth(self._app_id, self.to_data())
        if response:
            self.apply_data(response)


class OAuthClient:
    """Define an oauth client information."""

    def __init__(self, data: Optional[dict]):
        """Create a new instance of the OAuthClient."""
        self._client_id = None
        self._client_secret = None
        if data:
            self.apply_data(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        self._client_id = data['oauthClientId']
        self._client_secret = data['oauthClientSecret']

    @property
    def client_id(self):
        """Get the client id."""
        return self._client_id

    @property
    def client_secret(self):
        """Get the client secret."""
        return self._client_secret


class OAuthToken:
    """Define oauth token information."""

    _api: OAuthAPI
    _access_token: str
    _refresh_token: str
    _expires_in: int
    _token_type: str
    _scope: List[str]

    def __init__(self, api: OAuthAPI, data: Optional[dict]):
        """Create a new instance of the OAuthToken class."""
        self._api = api
        self._access_token = None
        self._refresh_token = None
        self._expires_in = 0
        self._token_type = None
        self._scope = []
        if data:
            self.apply_data(data)

    def apply_data(self, data: dict):
        """Apply the given data to the entity."""
        self._access_token = data['access_token']
        self._token_type = data['token_type']
        self._refresh_token = data['refresh_token']
        self._expires_in = data['expires_in']
        data_scope = data['scope']
        if isinstance(data_scope, list):
            self._scope = data_scope
        if isinstance(data_scope, str):
            self._scope.clear()
            self._scope.append(data_scope)

    def refresh(self):
        """Refresh the auth and refresh tokens."""
        data = self._api.get_token(self._refresh_token)
        if data:
            self.apply_data(data)

    @property
    def access_token(self) -> str:
        """Get the access token for authentication."""
        return self._access_token

    @property
    def refresh_token(self) -> str:
        """Get the refresh token for obtaining new access tokens."""
        return self._refresh_token

    @property
    def expires_in(self) -> int:
        """Get the amount of time in seconds until the token expires."""
        return self._expires_in

    @property
    def token_type(self) -> str:
        """Get the type of token."""
        return self._token_type

    @property
    def scope(self) -> List[str]:
        """Get the scopes the token has permission to."""
        return self._scope
