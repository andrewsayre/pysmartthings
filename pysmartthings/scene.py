"""Define the scene module."""
from typing import Dict, Optional

from .api import Api
from .entity import Entity


class Scene:
    """Define a scene data entity."""

    def __init__(self):
        """Create a new instance of the Scene class."""
        self._color = None
        self._icon = None
        self._location_id = None
        self._name = None
        self._scene_id = None

    def apply_data(self, data: dict):
        """Apply the data structure to the class."""
        self._color = data["sceneColor"]
        self._icon = data["sceneIcon"]
        self._location_id = data["locationId"]
        self._name = data["sceneName"]
        self._scene_id = data["sceneId"]

    @property
    def color(self) -> str:
        """Get the color of the scene."""
        return self._color

    @property
    def icon(self) -> str:
        """Get the icon of the scene."""
        return self._icon

    @property
    def location_id(self) -> str:
        """Get the location this scene is in."""
        return self._location_id

    @property
    def name(self) -> str:
        """Get the name of the scene."""
        return self._name

    @property
    def scene_id(self) -> str:
        """Get the id of the scene."""
        return self._scene_id


class SceneEntity(Entity, Scene):
    """Define a scene entity."""

    def __init__(self, api: Api, data: Optional[Dict] = None):
        """Create a new instance of the class."""
        Entity.__init__(self, api)
        Scene.__init__(self)
        if data:
            self.apply_data(data)

    async def execute(self):
        """Execute the scene."""
        result = await self._api.execute_scene(self._scene_id)
        return result == {"status": "success"}

    async def refresh(self):
        """Refresh is not implemented."""
        raise NotImplementedError()

    async def save(self):
        """Save is not implemented."""
        raise NotImplementedError()
