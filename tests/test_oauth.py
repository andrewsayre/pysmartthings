"""Tests for the OAuth module."""

import pytest

from pysmartthings.api import api_old
from pysmartthings.oauth import OAuth, OAuthEntity, OAuthToken
from pysmartthings.oauthapi import OAuthAPI

from . import api_mock
from .utilities import get_json


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
        api = api_old(api_mock.API_TOKEN)
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
        api = api_old(api_mock.API_TOKEN)
        entity = OAuthEntity(
            api, 'c6cde2b0-203e-44cf-a510-3b3ed4706996', None)
        entity.client_name = 'pysmartthings-test'
        entity.scope.append('r:devices')
        # Act/Assert
        entity.save()


class TestOAuthToken:
    """Tests for the OAuthToken class."""

    @staticmethod
    def test_init():
        """Tests the init method."""
        # Arrange/Act
        token = OAuthToken(None, None)
        # Assert
        assert token.expires_in == 0
        assert token.scope == []

    @staticmethod
    def test_apply_data():
        """Tests the apply data method."""
        # Arrange
        data = get_json('token_response.json')
        # Act
        token = OAuthToken(None, data)
        # Assert
        assert token.expires_in == 299
        assert token.refresh_token == '3d1a8d0a-a312-45c2-a9f5-95e59dc0e879'
        assert token.access_token == 'ad0fbf27-48d4-4ee9-ba47-7f5fedd7be35'
        assert token.token_type == 'bearer'
        assert token.scope == ['r:devices:*']

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = OAuthAPI(api_mock.CLIENT_ID, api_mock.CLIENT_SECRET)
        token = OAuthToken(api, refresh_token=api_mock.REFRESH_TOKEN)
        # Act
        token.refresh()
        # Assert
        assert token.refresh_token == '3d1a8d0a-a312-45c2-a9f5-95e59dc0e879'
