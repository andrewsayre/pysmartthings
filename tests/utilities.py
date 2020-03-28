"""Define testing utilities."""
import json as _json
from typing import Optional, Sequence, Union
from urllib.parse import parse_qs

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from yarl import URL

BodyFixtureType = Optional[Union[str, list, dict]]
BodyType = Optional[Union[list, dict]]


def get_json(file):
    """Load a json file."""
    with open("tests/json/" + file, "r") as json_file:
        return _json.load(json_file)


def _get_json_fixture(body: BodyFixtureType) -> BodyType:
    if isinstance(body, (dict, list)):
        return body
    if isinstance(body, str):
        return get_json(body + ".json")
    return None


class ClientMocker:
    """Mock Aiohttp client requests."""

    def __init__(self):
        """Initialize the request mocker."""
        self._mocks = []
        self.default_headers = None
        self.base_url = None

    def get(self, resource: str, *, params=None, response=None):
        """Register a mock get request."""
        self.request(
            "get",
            self.base_url + resource,
            params=params,
            headers=self.default_headers,
            response=response,
        )

    def post(self, resource: str, *, params=None, request=None, response=None):
        """Register a mock post request."""
        self.request(
            "post",
            self.base_url + resource,
            params=params,
            headers=self.default_headers,
            request=request,
            response=response,
        )

    def put(self, resource: str, *, params=None, request=None, response=None):
        """Register a mock post request."""
        self.request(
            "put",
            self.base_url + resource,
            params=params,
            headers=self.default_headers,
            request=request,
            response=response,
        )

    def delete(self, resource: str, *, params=None, response=None):
        """Register a mock get request."""
        self.request(
            "delete",
            self.base_url + resource,
            params=params,
            headers=self.default_headers,
            response=response,
        )

    def request(
        self,
        method: str,
        url: str,
        *,
        params=None,
        status=200,
        headers=None,
        request=None,
        response=None
    ):
        """Register a mock request."""
        self._mocks.append(
            MockResponse(method, url, params, status, headers, request, response)
        )

    def create_session(self, loop):
        """Create a ClientSession that is bound to this mocker."""
        session = ClientSession(loop=loop)
        # Setting directly on `session` will raise deprecation warning
        object.__setattr__(session, "_request", self.match_request)
        return session

    async def match_request(
        self,
        method,
        url,
        *,
        data=None,
        auth=None,
        params=None,
        headers=None,
        allow_redirects=None,
        timeout=None,
        json=None
    ):
        """Match a request against pre-registered requests."""
        url = URL(url)
        if params:
            url = url.with_query(params)

        for response in self._mocks:
            if response.match_request(method, url, headers or [], json):
                return response

        assert False, "No mock registered for {} {} {}".format(
            method.upper(), url, params
        )


class MockResponse:
    """Mock Aiohttp client response."""

    def __init__(self, method, url, params, status, headers, request, response):
        """Initialize a fake response."""
        self.method = method
        url = URL(url)
        if params:
            url = url.with_query(params)
        self._url = url
        self.status = status
        self._response = response
        self._request = request
        self._headers = headers or []

    def match_request(
        self, method: str, url: URL, headers: Optional[Sequence], json: BodyFixtureType
    ):
        """Test if response answers request."""
        # Headers
        if self._headers != headers:
            return False
        # Method
        if method.lower() != self.method.lower():
            return False
        # Url
        if (
            self._url.scheme != url.scheme
            or self._url.host != url.host
            or self._url.path != url.path
        ):
            return False
        # Query string
        request_qs = parse_qs(url.query_string)
        matcher_qs = parse_qs(self._url.query_string)
        if request_qs != matcher_qs:
            return False

        # Request body
        if self._request and not json == _get_json_fixture(self._request):
            return False
        return True

    @property
    def headers(self):
        """Return content_type."""
        return self._headers

    @property
    def cookies(self):
        """Return dict of cookies."""
        return {}

    @property
    def url(self):
        """Return yarl of URL."""
        return self._url

    @property
    def content(self):
        """Return content."""
        raise NotImplementedError

    async def read(self):
        """Return mock response."""
        raise NotImplementedError

    async def text(self, encoding="utf-8"):
        """Return mock response as a string."""
        raise NotImplementedError

    async def json(self, encoding="utf-8"):
        """Return mock response as a json."""
        return _get_json_fixture(self._response)

    def release(self):
        """Mock release."""
        pass

    def raise_for_status(self):
        """Raise error if status is 400 or higher."""
        if self.status >= 400:
            raise ClientResponseError(
                None, None, code=self.status, headers=self.headers
            )

    def close(self):
        """Mock close."""
        pass
