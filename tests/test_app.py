"""Define tests for the app module."""

import pytest

from pysmartthings.app import (APP_TYPE_LAMBDA, APP_TYPE_WEBHOOK,
                               CLASSIFICATION_AUTOMATION, App)
from .utilities import get_json


class TestApp:
    """Define tests for the App class."""

    @staticmethod
    def test_init():
        """Tests the load function."""
        # Arrange
        data = get_json('app_get.json')
        # Act
        app = App(None, data)
        # Assert
        assert app.app_id == "c6cde2b0-203e-44cf-a510-3b3ed4706996"
        assert app.app_name == "pysmartthings-test"
        assert app.app_type == "WEBHOOK_SMART_APP"
        assert app.classifications == [CLASSIFICATION_AUTOMATION]
        assert app.display_name == "Test"
        assert app.description == \
            "A SmartApp that relays events to the pysmartthings library"
        assert app.single_instance
        assert app.webhook_target_url == \
            "https://homeassistant.sayre.net:8321/"
        assert app.webhook_public_key
        assert app.created_date == "2018-12-15T17:07:41Z"
        assert app.last_updated_date == "2018-12-15T17:07:42Z"

    @staticmethod
    def test_app_name():
        """Tests get/set of app_name."""
        # Arrange
        app = App(None, None)
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
        app = App(None, None)
        # Act/Assert
        with pytest.raises(ValueError):
            app.app_name = ''
        with pytest.raises(ValueError):
            app.app_name = None
        with pytest.raises(ValueError):
            app.app_name = "My Super Cool App"

    @staticmethod
    def test_display_name():
        """Tests get/set of display_name."""
        # Arrange
        app = App(None, None)
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
        app = App(None, None)
        # Act/Assert
        with pytest.raises(ValueError):
            app.display_name = ''
        with pytest.raises(ValueError):
            app.display_name = None
        with pytest.raises(ValueError):
            app.display_name = 'x' * 76

    @staticmethod
    def test_description():
        """Tests get/set of description."""
        # Arrange
        app = App(None, None)
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
        app = App(None, None)
        # Act/Assert
        with pytest.raises(ValueError):
            app.description = ''
        with pytest.raises(ValueError):
            app.description = None
        with pytest.raises(ValueError):
            app.description = 'x' * 251

    @staticmethod
    def test_single_instance():
        """Tests get/set of single_instance."""
        # Arrange
        app = App(None, None)
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
        app = App(None, None)
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
        app = App(None, None)
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
        app = App(None, None)
        # Act/Assert
        with pytest.raises(ValueError):
            app.app_type = ''
        with pytest.raises(ValueError):
            app.app_type = None
        with pytest.raises(ValueError):
            app.app_type = 'Some type'

    @staticmethod
    def test_lambda_functions():
        """Tests get of lambda_functions."""
        # Arrange
        app = App(None, None)
        # Act
        app.lambda_functions.append(
            "arn:aws:lambda:eu-central-1:account-id:"
            "function:function-name:alias-name")
        # Assert
        assert app.lambda_functions
