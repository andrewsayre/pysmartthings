"""Tests for the scene module."""
from pysmartthings.scene import Scene, SceneEntity
import pytest

from .utilities import get_json


class TestScene:
    """Tests for the scene class."""

    @staticmethod
    def test_apply_data():
        """Test the init method."""
        # Arrange
        data = get_json("scenes.json")
        scene = Scene()
        scene.apply_data(data["items"][0])
        # Assert
        assert scene.scene_id == "3a570170-7c10-4e5a-bef8-0d02175798f2"
        assert scene.color == "#F7F9FF"
        assert scene.name == "Test"
        assert scene.location_id == "3b44ae84-a735-4fdd-8edd-fc295f4e1563"
        assert scene.icon == "st.scenes.wand"


class TestSceneEntity:
    """Tests for the scene entity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_execute(api):
        """Tests the execute method."""
        # Arrange
        data = get_json("scenes.json")
        entity = SceneEntity(api, data["items"][1])
        # Act
        result = await entity.execute()
        # Assert
        assert result

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        entity = SceneEntity(api)
        with pytest.raises(NotImplementedError):
            await entity.refresh()

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the refresh method."""
        entity = SceneEntity(api)
        with pytest.raises(NotImplementedError):
            await entity.save()
