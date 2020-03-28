"""Tests for the subscription module."""

from pysmartthings.subscription import SourceType, Subscription, SubscriptionEntity
import pytest

from .conftest import INSTALLED_APP_ID
from .utilities import get_json


class TestSubscription:
    """Tests for the Subscription class."""

    @staticmethod
    def test_init():
        """Test the initialization method."""
        # Arrange/Act
        sub = Subscription()
        # Assert
        assert sub.source_type is SourceType.UNKNOWN
        assert sub.capability == "*"
        assert sub.attribute == "*"
        assert sub.value == "*"
        assert sub.state_change_only

    @staticmethod
    def test_apply_data_capability():
        """Test apply data."""
        # Arrange
        data = get_json("subscription_capability_get_response.json")
        sub = Subscription()
        # Act
        sub.apply_data(data)
        # Assert
        assert sub.subscription_id == "7bdf5909-57c4-41f3-9089-e520513bd92a"
        assert sub.installed_app_id == INSTALLED_APP_ID
        assert sub.source_type == SourceType.CAPABILITY
        assert sub.location_id == "397678e5-9995-4a39-9d9f-ae6ba310236b"
        assert sub.capability == "switchLevel"
        assert sub.attribute == "*"
        assert sub.value == "*"
        assert sub.state_change_only
        assert sub.subscription_name == "switchLevel_sub"

    @staticmethod
    def test_apply_data_device():
        """Test apply data."""
        # Arrange
        data = get_json("subscription_device_get_response.json")
        sub = Subscription()
        # Act
        sub.apply_data(data)
        # Assert
        assert sub.subscription_id == "498752fd-db87-4a5e-95f5-25a0e412838d"
        assert sub.installed_app_id == INSTALLED_APP_ID
        assert sub.source_type == SourceType.DEVICE
        assert sub.device_id == "64e7f664-5b99-4573-b76d-03be3021dc78"
        assert sub.component_id == "*"
        assert sub.capability == "*"
        assert sub.attribute == "*"
        assert sub.value == "*"
        assert sub.state_change_only
        assert not sub.subscription_name

    @staticmethod
    def test_to_data_capability():
        """Test the to_data method for capabilities."""
        # Arrange
        sub = Subscription()
        sub.source_type = SourceType.CAPABILITY
        sub.location_id = "397678e5-9995-4a39-9d9f-ae6ba310236b"
        sub.capability = "switch"
        sub.attribute = "switchLevel"
        sub.value = "100"
        sub.state_change_only = False
        sub.subscription_name = "Test"
        # Act
        data = sub.to_data()
        # Assert
        assert data["sourceType"] == SourceType.CAPABILITY.value
        assert (
            data["capability"]["locationId"] == "397678e5-9995-4a39-9d9f-ae6ba310236b"
        )
        assert data["capability"]["capability"] == "switch"
        assert data["capability"]["attribute"] == "switchLevel"
        assert data["capability"]["value"] == "100"
        assert data["capability"]["subscriptionName"] == "Test"
        assert not data["capability"]["stateChangeOnly"]

    @staticmethod
    def test_to_data_device():
        """Test the to_data method for devices."""
        # Arrange
        sub = Subscription()
        sub.source_type = SourceType.DEVICE
        sub.device_id = "397678e5-9995-4a39-9d9f-ae6ba310236b"
        sub.component_id = "main"
        sub.capability = "switch"
        sub.attribute = "switchLevel"
        sub.value = "100"
        sub.state_change_only = True
        sub.subscription_name = "Test"
        # Act
        data = sub.to_data()
        # Assert
        assert data["sourceType"] == SourceType.DEVICE.value
        assert data["device"]["deviceId"] == "397678e5-9995-4a39-9d9f-ae6ba310236b"
        assert data["device"]["componentId"] == "main"
        assert data["device"]["capability"] == "switch"
        assert data["device"]["attribute"] == "switchLevel"
        assert data["device"]["value"] == "100"
        assert data["device"]["subscriptionName"] == "Test"
        assert data["device"]["stateChangeOnly"]


class TestSubscriptionEntity:
    """Tests for the SubscriptionEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        app = SubscriptionEntity(api)
        app.apply_data(
            {
                "id": "7bdf5909-57c4-41f3-9089-e520513bd92a",
                "installedAppId": INSTALLED_APP_ID,
                "sourceType": "UNKNOWN",
            }
        )
        # Act
        await app.refresh()
        # Assert
        assert app.subscription_name == "switchLevel_sub"

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the refresh method."""
        # Arrange
        app = SubscriptionEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            await app.save()
