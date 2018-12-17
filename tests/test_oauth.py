"""Tests for the OAuth module."""

import pytest

from pysmartthings.api import API
from pysmartthings.oauth import OAuth, OAuthEntity

from . import api_mock


class TestOAuth:
    """Tests for the OAuth class."""

    @staticmethod
    def test_init():
        """Tests the initialization."""
        # Arrange
        app_id = '5c03e518-118a-44cb-85ad-7877d0b302e4'
        # Act
        oauth = OAuth(app_id)
        # Assert
        assert app_id == oauth.app_id
        assert oauth.scope is not None

    @staticmethod
    def test_client_name():
        """Tests get/set of client name."""
        # Arrange
        oauth = OAuth('5c03e518-118a-44cb-85ad-7877d0b302e4')
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
        oauth = OAuth('5c03e518-118a-44cb-85ad-7877d0b302e4')
        # Act/Assert
        with pytest.raises(ValueError):
            oauth.client_name = ''


class TestOAuthEntity:
    """Tests for the OAuthEntity class."""

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        entity = OAuthEntity(
            api, 'c6cde2b0-203e-44cf-a510-3b3ed4706996', None)
        # Act
        entity.refresh()
        # Assert
        assert entity.client_name == 'pysmartthings-test'
        assert 'r:devices' in entity.scope

    @staticmethod
    def test_save(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        entity = OAuthEntity(
            api, 'c6cde2b0-203e-44cf-a510-3b3ed4706996', None)
        entity.client_name = 'pysmartthings-test'
        entity.scope.append('r:devices')
        # Act/Assert
        entity.save()
