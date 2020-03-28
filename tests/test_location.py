"""Tests for the Location module."""

from pysmartthings.location import Location, LocationEntity
import pytest

from .conftest import LOCATION_ID
from .utilities import get_json


class TestLocation:
    """Tests for the Location class."""

    @staticmethod
    def test_apply_data():
        """Tests the apply_data function."""
        # Arrange
        data = get_json("location.json")
        location = Location()
        # Act
        location.apply_data(data)
        # Assert
        assert location.location_id == LOCATION_ID
        assert location.name == "Test Home"
        assert location.country_code == "USA"
        assert location.latitude == 45.00708112
        assert location.longitude == -93.11223629
        assert location.region_radius == 150
        assert location.temperature_scale == "F"
        assert location.timezone_id is None
        assert location.locale == "en"


class TestLocationEntity:
    """Tests the LocationEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        entity = LocationEntity(api, location_id=LOCATION_ID)
        # Act
        await entity.refresh()
        # Assert
        assert entity.name == "Test Home"

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the save method."""
        # Arrange
        entity = LocationEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            await entity.save()

    @staticmethod
    @pytest.mark.asyncio
    async def test_rooms(api):
        """Tests the refresh method."""
        # Arrange
        entity = LocationEntity(api, location_id=LOCATION_ID)
        # Act
        rooms = await entity.rooms()
        # Assert
        assert len(rooms) == 1
