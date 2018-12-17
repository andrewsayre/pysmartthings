"""Define the oauth module."""

from typing import List

from .api import API
from .entity import Entity


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
