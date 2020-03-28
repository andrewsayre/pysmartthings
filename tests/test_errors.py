"""Tests for the error module."""

from pysmartthings.errors import APIResponseError


class TestAPIResponseError:
    """Tests for the APIResponseError class."""

    @staticmethod
    def test_is_target_error():
        """Tests the initialization."""
        # Arrange/Act
        data = {
            "requestId": "8B66A345-03B0-477F-A8A6-1A1CF0277040",
            "error": {
                "code": "ConstraintViolationError",
                "message": "The request is malformed.",
                "details": [
                    {
                        "code": "TargetTimeoutError",
                        "target": "https://blah.blah/blah",
                        "message": "Upstream target timed out",
                        "details": [],
                    }
                ],
            },
        }
        error = APIResponseError(None, None, data=data)
        # Assert
        assert error.is_target_error()
        assert error.raw_error_response == data
        assert error.request_id == "8B66A345-03B0-477F-A8A6-1A1CF0277040"
        assert error.error.code == "ConstraintViolationError"
        assert error.error.message == "The request is malformed."
        assert len(error.error.details) == 1
        detail = error.error.details[0]
        assert detail.code == "TargetTimeoutError"
        assert detail.target == "https://blah.blah/blah"
        assert detail.message == "Upstream target timed out"
        assert not detail.details

    @staticmethod
    def test_str():
        """Tests the initialization."""
        # Arrange/Act
        data = {"requestId": "8B66A345-03B0-477F-A8A6-1A1CF0277040"}
        error = APIResponseError(
            None, None, status=422, message="Unprocessable Entity", data=data
        )
        # Assert
        assert (
            str(error) == "Unprocessable Entity (422): "
            '{"requestId": "8B66A345-03B0-477F-A8A6-1A1CF0277040"}'
        )
