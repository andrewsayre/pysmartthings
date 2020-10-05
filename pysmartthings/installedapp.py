"""Define the installedapp module."""

from enum import Enum
from typing import Sequence

from .api import Api
from .entity import Entity
from .subscription import SubscriptionEntity


def format_install_url(app_id: str, location_id: str) -> str:
    """Return a web-based URL to auth and install a SmartApp."""
    return f"https://account.smartthings.com/login?redirect=https%3A%2F%2Fstrongman-regional.api.smartthings.com%2F%3FappId%3D{app_id}%26locationId%3D{location_id}%26appType%3DENDPOINTAPP%26language%3Den%26clientOS%3Dweb"


class InstalledAppType(Enum):
    """Define the type of installed app."""

    UNKNOWN = "UNKNOWN"
    LAMBDA_SMART_APP = "LAMBDA_SMART_APP"
    WEBHOOK_SMART_APP = "WEBHOOK_SMART_APP"
    BEHAVIOR = "BEHAVIOR"


class InstalledAppStatus(Enum):
    """Define the installed app status."""

    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    REVOKED = "REVOKED"
    DISABLED = "DISABLED"


class InstalledApp:
    """Define the InstalledApp class."""

    def __init__(self):
        """Create a new instance of the InstalledApp class."""
        self._installed_app_id = None
        self._installed_app_type = InstalledAppType.UNKNOWN
        self._installed_app_status = InstalledAppStatus.UNKNOWN
        self._display_name = None
        self._app_id = None
        self._reference_id = None
        self._location_id = None
        self._created_date = None
        self._last_updated_date = None
        self._classifications = []

    def apply_data(self, data: dict):
        """Apply the data structure to the properties."""
        self._installed_app_id = data["installedAppId"]
        self._installed_app_type = InstalledAppType(data["installedAppType"])
        self._installed_app_status = InstalledAppStatus(data["installedAppStatus"])
        self._display_name = data["displayName"]
        self._app_id = data["appId"]
        self._reference_id = data["referenceId"]
        self._location_id = data["locationId"]
        self._created_date = data["createdDate"]
        self._last_updated_date = data["lastUpdatedDate"]
        self._classifications = data["classifications"]

    @property
    def installed_app_id(self) -> str:
        """Get the ID of the installed app."""
        return self._installed_app_id

    @property
    def installed_app_type(self) -> InstalledAppType:
        """Get the type of installed app."""
        return self._installed_app_type

    @property
    def installed_app_status(self) -> InstalledAppStatus:
        """Get the current state of an install."""
        return self._installed_app_status

    @property
    def display_name(self) -> str:
        """Get the user defined name for the installed app."""
        return self._display_name

    @property
    def app_id(self) -> str:
        """Get the ID of the app."""
        return self._app_id

    @property
    def reference_id(self) -> str:
        """Get a reference to an upstream system."""
        return self._reference_id

    @property
    def location_id(self) -> str:
        """Get the ID of the location to which the installed app."""
        return self._location_id

    @property
    def created_date(self) -> str:
        """Get the date the installed app was created."""
        return self._created_date

    @property
    def last_updated_date(self) -> str:
        """Get the date the installed app was updated."""
        return self._last_updated_date

    @property
    def classifications(self) -> Sequence[str]:
        """Get the collection of classifications."""
        return self._classifications


class InstalledAppEntity(Entity, InstalledApp):
    """Define the InstalledAppEntity class."""

    def __init__(self, api: Api, data=None, installed_app_id=None):
        """Create a new instance of the InstalledAppEntity class."""
        Entity.__init__(self, api)
        InstalledApp.__init__(self)
        if data:
            self.apply_data(data)
        if installed_app_id:
            self._installed_app_id = installed_app_id

    async def refresh(self):
        """Refresh the installedapp information using the API."""
        data = await self._api.get_installed_app(self._installed_app_id)
        self.apply_data(data)

    async def save(self):
        """Save the changes made to the app."""
        raise NotImplementedError

    async def subscriptions(self) -> Sequence[SubscriptionEntity]:
        """Get the subscriptions for the installedapp."""
        data = await self._api.get_subscriptions(self._installed_app_id)
        return [SubscriptionEntity(self._api, entity) for entity in data]
