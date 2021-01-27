"""Define consts for the pysmartthings package."""

__title__ = "pysmartthings"
__version__ = "0.7.7"

# Constants for Health
HEALTH_API_STATE = "state"
HEALTH_PACKAGE_STATE = "state"
HEALTH_API_LAST_UPDATE = "lastUpdatedDate"
HEALTH_PACKAGE_LAST_UPDATE = "lastUpdatedDate"
HEALTH_ATTRIBUTE_MAP = {
    HEALTH_API_STATE: HEALTH_PACKAGE_STATE,
    HEALTH_API_LAST_UPDATE: HEALTH_PACKAGE_LAST_UPDATE,
}
