"""A python library for interacting with the SmartThings cloud API."""

from .app import (
    APP_TYPE_LAMBDA,
    APP_TYPE_WEBHOOK,
    CLASSIFICATION_AUTOMATION,
    App,
    AppEntity,
    AppOAuth,
    AppOAuthClient,
    AppOAuthClientEntity,
    AppOAuthEntity,
    AppSettings,
    AppSettingsEntity,
)
from .capability import (
    ATTRIBUTES,
    CAPABILITIES,
    CAPABILITIES_TO_ATTRIBUTES,
    Attribute,
    Capability,
)
from .const import __title__, __version__  # noqa
from .device import (
    DEVICE_TYPE_DTH,
    DEVICE_TYPE_ENDPOINT_APP,
    DEVICE_TYPE_OCF,
    DEVICE_TYPE_UNKNOWN,
    DEVICE_TYPE_VIPER,
    Command,
    Device,
    DeviceEntity,
    DeviceStatus,
    DeviceStatusBase,
)
from .errors import APIErrorDetail, APIInvalidGrant, APIResponseError
from .installedapp import (
    InstalledApp,
    InstalledAppEntity,
    InstalledAppStatus,
    InstalledAppType,
)
from .location import Location, LocationEntity
from .oauthtoken import OAuthToken
from .room import Room, RoomEntity
from .scene import Scene, SceneEntity
from .smartthings import SmartThings
from .subscription import SourceType, Subscription, SubscriptionEntity

__all__ = [
    # app
    "APP_TYPE_LAMBDA",
    "APP_TYPE_WEBHOOK",
    "CLASSIFICATION_AUTOMATION",
    "App",
    "AppEntity",
    "AppOAuth",
    "AppOAuthClient",
    "AppOAuthClientEntity",
    "AppOAuthEntity",
    "AppSettings",
    "AppSettingsEntity",
    # capability
    "ATTRIBUTES",
    "CAPABILITIES",
    "CAPABILITIES_TO_ATTRIBUTES",
    "Attribute",
    "Capability",
    # device
    "DEVICE_TYPE_DTH",
    "DEVICE_TYPE_ENDPOINT_APP",
    "DEVICE_TYPE_OCF",
    "DEVICE_TYPE_UNKNOWN",
    "DEVICE_TYPE_VIPER",
    "Command",
    "Device",
    "DeviceEntity",
    "DeviceStatus",
    "DeviceStatusBase",
    # error
    "APIErrorDetail",
    "APIInvalidGrant",
    "APIResponseError",
    # installed app
    "InstalledApp",
    "InstalledAppEntity",
    "InstalledAppStatus",
    "InstalledAppType",
    # location
    "Location",
    "LocationEntity",
    # room
    "Room",
    "RoomEntity",
    # oauthtoken
    "OAuthToken",
    # scene
    "Scene",
    "SceneEntity",
    # smartthings
    "SmartThings",
    # subscription
    "SourceType",
    "Subscription",
    "SubscriptionEntity",
]
