"""Tests for the room module."""
from pysmartthings.room import Room, RoomEntity
import pytest

from .conftest import LOCATION_ID, ROOM_ID
from .utilities import get_json


class TestRoom:
    """Tests for the Room class."""

    @staticmethod
    def test_apply_data():
        """Test the init method."""
        # Arrange
        data = get_json("room.json")
        room = Room()
        room.apply_data(data)
        # Assert
        assert room.room_id == ROOM_ID
        assert room.location_id == LOCATION_ID
        assert room.name == "Theater"
        assert room.background_image == "Test"


class TestRoomEntity:
    """Tests for the room entity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        entity = RoomEntity(api, location_id=LOCATION_ID, room_id=ROOM_ID)
        # Act
        await entity.refresh()
        # Assert
        assert entity.name == "Theater"

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the save method."""
        # Arrange
        entity = RoomEntity(api, location_id=LOCATION_ID, room_id=ROOM_ID)
        entity.name = "Theater"
        entity.background_image = "Test"
        # Act
        await entity.save()
        # Assert
        assert entity.name == "Theater"
        assert entity.background_image == "Test"
