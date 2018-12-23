"""Tests for the Location module."""

import pytest

from pysmartthings.api import API
from pysmartthings.location import Location, LocationEntity

from . import api_mock
from .utilities import get_json


class TestLocation:
    """Tests for the Location class."""

    @staticmethod
    def test_apply_data():
        """Tests the apply_data function."""
        # Arrange
        data = get_json('location.json')
        location = Location()
        # Act
        location.apply_data(data)
        # Assert
        assert location.location_id == api_mock.LOCATION_ID
        assert location.name == "Test Home"
        assert location.country_code == 'USA'
        assert location.latitude == 45.00708112
        assert location.longitude == -93.11223629
        assert location.region_radius == 150
        assert location.temperature_scale == 'F'
        assert location.timezone_id is None
        assert location.locale == 'en'


class TestLocationEntity:
    """Tests the LocationEntity class."""

    @staticmethod
    def test_refresh(requests_mock):
        """Tests the refresh method."""
        # Arrange
        api_mock.setup(requests_mock)
        api = API(api_mock.API_TOKEN)
        location = LocationEntity(api, location_id=api_mock.LOCATION_ID)
        # Act
        location.refresh()
        # Assert
        assert location.name == 'Test Home'

    @staticmethod
    def test_save():
        """Tests the save method."""
        # Arrange
        api = API(api_mock.API_TOKEN)
        location = LocationEntity(api)
        # Act/Assert
        with pytest.raises(NotImplementedError):
            location.save()
