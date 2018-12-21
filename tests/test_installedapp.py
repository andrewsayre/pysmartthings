"""Tests for the installedapp module."""

import pytest

from pysmartthings.api import API
from pysmartthings.installedapp import (
    InstalledApp, InstalledAppEntity, InstalledAppStatus, InstalledAppType)

from . import api_mock
from .utilities import get_json


class TestInstalledApp:
    """Tests for the InstalledApp class."""

    @staticmethod
    def test_init():
        """Tests the initialization."""
        # Arrange/Act
        app = InstalledApp()
        # Assert
        assert app.installed_app_type is InstalledAppType.UNKNOWN
        assert app.installed_app_status is InstalledAppStatus.UNKNOWN
        assert app.classifications == []

    @staticmethod
    def test_apply_data():
        """Tests the apply_data function."""
        # Arrange
        app = InstalledApp()
        data = get_json('installedapp_get_response.json')
        # Act
        app.apply_data(data)
        # Assert
        assert app.installed_app_id == api_mock.INSTALLED_APP_ID
        assert app.installed_app_type == InstalledAppType.WEBHOOK_SMART_APP
        assert app.installed_app_status == InstalledAppStatus.PENDING
        assert app.display_name == 'pysmartthings'
        assert app.app_id == api_mock.APP_ID
        assert app.reference_id is None
        assert app.location_id == '397678e5-9995-4a39-9d9f-ae6ba310236b'
        assert app.created_date == '2018-12-19T02:49:58Z'
        assert app.last_updated_date == '2018-12-19T02:49:58Z'
        assert app.classifications == ['AUTOMATION']


class TestInstalledAppEntity:
    """Tests for the InstalledAppEntity class."""

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = InstalledAppEntity(
            api, installed_app_id=api_mock.INSTALLED_APP_ID)
        # Act
        app.refresh()
        # Assert
        assert app.app_id == api_mock.APP_ID

    @staticmethod
    def test_save():
        """Tests the refresh method."""
        # Arrange
        api = API(api_mock.API_TOKEN)
        app = InstalledAppEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            app.save()

    @staticmethod
    def test_subscriptions(requests_mock):
        """Tests the subscriptions method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        app = InstalledAppEntity(
            api, installed_app_id=api_mock.INSTALLED_APP_ID)
        app.refresh()
        # Act
        subscriptions = app.subscriptions()
        # Assert
        assert len(subscriptions) == 3