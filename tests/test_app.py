"""Define tests for the app module."""

from pysmartthings.app import (
    APP_TYPE_LAMBDA,
    APP_TYPE_WEBHOOK,
    CLASSIFICATION_AUTOMATION,
    App,
    AppEntity,
    AppOAuth,
    AppOAuthEntity,
    AppSettings,
    AppSettingsEntity,
)
import pytest

from .conftest import APP_ID
from .utilities import get_json


class TestApp:
    """Define tests for the App class."""

    @staticmethod
    def test_init():
        """Tests the init function."""
        # Arrange/Act
        app = App()
        # Assert
        assert app.classifications is not None
        assert app.lambda_functions is not None

    @staticmethod
    def test_apply_data():
        """Tests the apply_data function."""
        # Arrange
        app = App()
        data = get_json("app_get.json")
        # Act
        app.apply_data(data)
        # Assert
        assert app.app_id == "c6cde2b0-203e-44cf-a510-3b3ed4706996"
        assert app.app_name == "pysmartthings-test"
        assert app.app_type == "WEBHOOK_SMART_APP"
        assert app.classifications == [CLASSIFICATION_AUTOMATION]
        assert app.display_name == "Test"
        assert (
            app.description
            == "A SmartApp that relays events to the pysmartthings library"
        )
        assert app.single_instance
        assert app.webhook_target_url == "https://homeassistant.sayre.net:8321/"
        assert app.webhook_public_key
        assert app.created_date == "2018-12-15T17:07:41Z"
        assert app.last_updated_date == "2018-12-15T17:07:42Z"

    @staticmethod
    def test_app_name():
        """Tests get/set of app_name."""
        # Arrange
        app = App()
        # Act
        expected_app_name = "my_app"
        app.app_name = expected_app_name
        app_name = app.app_name
        # Assert
        assert app_name == expected_app_name

    @staticmethod
    def test_app_name_invalid():
        """Tests valid values of app_name."""
        # Arrange
        app = App()
        # Act/Assert
        with pytest.raises(ValueError):
            app.app_name = ""
        with pytest.raises(ValueError):
            app.app_name = None
        with pytest.raises(ValueError):
            app.app_name = "My Super Cool App"

    @staticmethod
    def test_display_name():
        """Tests get/set of display_name."""
        # Arrange
        app = App()
        # Act
        expected = "My Display Name"
        app.display_name = expected
        actual = app.display_name
        # Assert
        assert expected == actual

    @staticmethod
    def test_display_name_invalid():
        """Tests valid values of display_name."""
        # Arrange
        app = App()
        # Act/Assert
        with pytest.raises(ValueError):
            app.display_name = ""
        with pytest.raises(ValueError):
            app.display_name = None
        with pytest.raises(ValueError):
            app.display_name = "x" * 76

    @staticmethod
    def test_description():
        """Tests get/set of description."""
        # Arrange
        app = App()
        # Act
        expected = "My Description"
        app.description = expected
        actual = app.description
        # Assert
        assert expected == actual

    @staticmethod
    def test_description_invalid():
        """Tests valid values of description."""
        # Arrange
        app = App()
        # Act/Assert
        with pytest.raises(ValueError):
            app.description = ""
        with pytest.raises(ValueError):
            app.description = None
        with pytest.raises(ValueError):
            app.description = "x" * 251

    @staticmethod
    def test_single_instance():
        """Tests get/set of single_instance."""
        # Arrange
        app = App()
        # Act
        expected = True
        app.single_instance = expected
        actual = app.single_instance
        # Assert
        assert expected == actual

    @staticmethod
    def test_app_type_webhook():
        """Tests get/set of app_type to webhook."""
        # Arrange
        app = App()
        # Act
        expected = APP_TYPE_WEBHOOK
        app.app_type = expected
        actual = app.app_type
        # Assert
        assert expected == actual

    @staticmethod
    def test_app_type_lambda():
        """Tests get/set of app_type to labmda."""
        # Arrange
        app = App()
        # Act
        expected = APP_TYPE_LAMBDA
        app.app_type = expected
        actual = app.app_type
        # Assert
        assert expected == actual

    @staticmethod
    def test_app_type_invalid():
        """Tests valid values of app_type."""
        # Arrange
        app = App()
        # Act/Assert
        with pytest.raises(ValueError):
            app.app_type = ""
        with pytest.raises(ValueError):
            app.app_type = None
        with pytest.raises(ValueError):
            app.app_type = "Some type"

    @staticmethod
    def test_lambda_functions():
        """Tests get of lambda_functions."""
        # Arrange
        app = App()
        # Act
        app.lambda_functions.append(
            "arn:aws:lambda:eu-central-1:account-id:"
            "function:function-name:alias-name"
        )
        # Assert
        assert app.lambda_functions

    @staticmethod
    def test_webhook_target_url():
        """Tests get/set of webhook_target_url."""
        # Arrange
        app = App()
        # Act
        expected = "http://my.web.site/"
        app.webhook_target_url = expected
        actual = app.webhook_target_url
        # Assert
        assert expected == actual


class TestAppSettings:
    """Tests for the AppSettings class."""

    @staticmethod
    def test_init():
        """Tests the init method."""
        # Arrange/Act
        settings = AppSettings(APP_ID)
        # Assert
        assert settings.app_id == APP_ID

    @staticmethod
    def test_apply_data():
        """Tests the apply_data method."""
        # Arrange
        data = get_json("app_settings.json")
        settings = AppSettings(APP_ID)
        # Act
        settings.apply_data(data)
        # Assert
        assert settings.settings["test"] == "test"

    @staticmethod
    def test_to_data():
        """Tests the to_data method."""
        # Arrange
        settings = AppSettings(APP_ID)
        settings.settings = {"test": "test"}
        # Act
        data = settings.to_data()
        # Assert
        assert data == {"settings": {"test": "test"}}


class TestAppSettingsEntity:
    """Tests for the AppSettingsEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests data is refreshed."""
        # Arrange
        data = {"settings": {"test2": "test"}}
        settings = AppSettingsEntity(api, APP_ID, data)
        # Act
        await settings.refresh()
        # Assert
        assert settings.settings == {"test": "test"}

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh_no_app_id(api):
        """Tests refresh when there's no app id."""
        # Arrange
        settings = AppSettingsEntity(api, None)
        # Act/Assert
        with pytest.raises(ValueError):
            await settings.refresh()

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the save function."""
        # Arrange
        data = {"settings": {"test": "test"}}
        settings = AppSettingsEntity(api, APP_ID, data)
        # Act
        await settings.save()
        # Assert
        assert settings.settings == {"test": "test"}

    @staticmethod
    @pytest.mark.asyncio
    async def test_save_no_app_id(api):
        """Tests save when there's no app id."""
        # Arrange
        settings = AppSettingsEntity(api, None)
        # Act/Assert
        with pytest.raises(ValueError):
            await settings.save()


class TestAppEntity:
    """Tests for the AppEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests data is refreshed."""
        # Arrange
        data = get_json("apps.json")["items"][0]
        app = AppEntity(api, data)
        # Act
        await app.refresh()
        # Assert
        assert app.single_instance
        assert app.webhook_target_url == "https://homeassistant.sayre.net:8321/"
        assert app.webhook_public_key

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests updating an entity."""
        # Arrange
        data = get_json("app_get.json")
        app = AppEntity(api, data)
        before = app.last_updated_date
        # Act
        await app.save()
        # Assert
        assert app.last_updated_date > before

    @staticmethod
    @pytest.mark.asyncio
    async def test_oauth(api):
        """Tests the oauth method."""
        # Arrange
        data = get_json("app_get.json")
        app = AppEntity(api, data)
        # Act
        oauth = await app.oauth()
        # Assert
        assert oauth.app_id == app.app_id
        assert oauth.client_name == "pysmartthings-test"
        assert oauth.scope == ["r:devices"]

    @staticmethod
    @pytest.mark.asyncio
    async def test_settings(api):
        """Tests the settings method."""
        # Arrange
        data = get_json("app_get.json")
        app = AppEntity(api, data)
        # Act
        settings = await app.settings()
        # Assert
        assert settings.settings == {"test": "test"}


class TestOAuth:
    """Tests for the OAuth class."""

    @staticmethod
    def test_init():
        """Tests the initialization."""
        # Arrange
        app_id = "5c03e518-118a-44cb-85ad-7877d0b302e4"
        # Act
        oauth = AppOAuth(app_id)
        # Assert
        assert app_id == oauth.app_id
        assert oauth.scope is not None

    @staticmethod
    def test_client_name():
        """Tests get/set of client name."""
        # Arrange
        oauth = AppOAuth("5c03e518-118a-44cb-85ad-7877d0b302e4")
        # Act
        expected = "my_app"
        oauth.client_name = expected
        actual = oauth.client_name
        # Assert
        assert actual == expected

    @staticmethod
    def test_client_name_invalid():
        """Tests setting an invalid client name."""
        # Arrange
        oauth = AppOAuth("5c03e518-118a-44cb-85ad-7877d0b302e4")
        # Act/Assert
        with pytest.raises(ValueError):
            oauth.client_name = ""


class TestOAuthEntity:
    """Tests for the OAuthEntity class."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        entity = AppOAuthEntity(api, "c6cde2b0-203e-44cf-a510-3b3ed4706996", None)
        # Act
        await entity.refresh()
        # Assert
        assert entity.client_name == "pysmartthings-test"
        assert "r:devices" in entity.scope

    @staticmethod
    @pytest.mark.asyncio
    async def test_save(api):
        """Tests the refresh method."""
        # Arrange
        entity = AppOAuthEntity(api, "c6cde2b0-203e-44cf-a510-3b3ed4706996", None)
        entity.client_name = "pysmartthings-test"
        entity.scope.append("r:devices")
        # Act/Assert
        await entity.save()
