"""Tests for the OAuth module."""

from pysmartthings.oauthtoken import OAuthToken
import pytest

from .conftest import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
from .utilities import get_json


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
        data = get_json("token_response.json")
        # Act
        token = OAuthToken(None, data)
        # Assert
        assert token.expires_in == 299
        assert token.refresh_token == "3d1a8d0a-a312-45c2-a9f5-95e59dc0e879"
        assert token.access_token == "ad0fbf27-48d4-4ee9-ba47-7f5fedd7be35"
        assert token.token_type == "bearer"
        assert token.scope == ["r:devices:*"]

    @staticmethod
    @pytest.mark.asyncio
    async def test_refresh(api):
        """Tests the refresh method."""
        # Arrange
        token = OAuthToken(api, refresh_token=REFRESH_TOKEN)
        # Act
        await token.refresh(CLIENT_ID, CLIENT_SECRET)
        # Assert
        assert token.refresh_token == "3d1a8d0a-a312-45c2-a9f5-95e59dc0e879"
