"""Define errors that can be returned from the SmartThings API."""
from typing import Optional, Sequence

from aiohttp import ClientResponseError

UNAUTHORIZED_ERROR = \
    "Authorization for the API is required, but the request has not been " \
    "authenticated."
FORBIDDEN_ERROR = \
    "The request has been authenticated but does not have appropriate" \
    "permissions, or a requested resource is not found."
UNKNOWN_ERROR = "An unknown API error occurred."


class APIErrorDetail:
    """Define details about an error."""

    def __init__(self, data):
        """Create a new instance of the error detail."""
        self._code = data.get('code')
        self._message = data.get('message')
        self._target = data.get('target')
        self._details = []
        details = data.get('details')
        if isinstance(details, list):
            self._details.extend(
                [APIErrorDetail(detail) for detail in details])

    @property
    def code(self) -> Optional[str]:
        """Get the SmartThings-defined error code."""
        return self._code

    @property
    def message(self) -> Optional[str]:
        """Get a description of the error."""
        return self._message

    @property
    def target(self) -> Optional[str]:
        """Get the target of the particular error."""
        return self._target

    @property
    def details(self) -> Sequence:
        """Get an array of errors that represent related errors."""
        return self._details


class APIResponseError(ClientResponseError):
    """Define an error from the API."""

    def __init__(self, request_info, history, *, status=None, message='',
                 headers=None, data=None):
        """Create a new instance of the API Error."""
        super().__init__(request_info, history, status=status,
                         message=message, headers=headers)
        self._request_id = data.get('requestId')
        self._error = APIErrorDetail(data['error'])

    @property
    def request_id(self) -> Optional[str]:
        """Get request correlation id."""
        return self._request_id

    @property
    def error(self) -> APIErrorDetail:
        """Get the API error document."""
        return self._error


class APIInvalidGrant(Exception):
    """Define an invalid grant error."""

    pass
