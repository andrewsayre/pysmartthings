"""Tests for the Location Mode module."""

import pytest

from pysmartthings.mode import Mode, ModeEntity

from .conftest import LOCATION_ID, MODE_ID
from .utilities import get_json


class TestMode:
    """Tests for the Location Mode class."""

    @staticmethod
    def test_apply_data():
        """Tests the apply_data function."""
        # Arrange
        data = get_json("mode.json")
        mode = Mode()
        # Act
        mode.apply_data(data)
        # Assert
        assert mode.mode_id == MODE_ID
        assert mode.location_id == LOCATION_ID
        assert mode.name == "Home"
        assert mode.label == "Home"
        assert mode.allowed == "['w:modes', 'd:modes']"
        assert mode.last_modified == "1653325206032"


class TestModeEntity:
    """Tests the ModeEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        entity = ModeEntity(api, location_id=LOCATION_ID, mode_id=MODE_ID)
        # Act
        await entity.refresh()
        # Assert
        assert entity.name == "Home"

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the save method."""
        # Arrange
        entity = ModeEntity(api, location_id=LOCATION_ID, mode_id=MODE_ID)
        entity.name = "Home"
        # Act
        await entity.save()
        # Assert
        assert entity.name == "Home"
