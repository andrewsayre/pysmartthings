"""Define errors that can be returned from the SmartThings API."""

UNAUTHORIZED_ERROR = \
    "Authorization for the API is required, but the request has not been " \
    "authenticated."
FORBIDDEN_ERROR = \
    "The request has been authenticated but does not have appropriate" \
    "permissions, or a requested resource is not found."
UNKNOWN_ERROR = "An unknown API error occurred."


class APIUnauthorizedError(Exception):
    """Define the error when the API key is invalid."""

    def __init__(self):
        """Initialize instance of APIUnauthorizedError."""
        Exception.__init__(self, UNAUTHORIZED_ERROR)


class APIForbiddenError(Exception):
    """Define the error when the API key does not have permission."""

    def __init__(self):
        """Initialize instance of APIForbiddenError."""
        Exception.__init__(self, FORBIDDEN_ERROR)


class APIUnknownError(Exception):
    """Define a general error condition."""

    def __init__(self):
        """Initialize instance of APIUnknownError."""
        Exception.__init__(self, UNKNOWN_ERROR)


class APIInvalidGrant(Exception):
    """Define an invalid grant error."""

    pass
