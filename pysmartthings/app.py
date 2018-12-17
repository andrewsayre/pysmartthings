"""Define the app module."""

import re
from typing import List, Optional

from .api import API
from .oauth import OAuthEntity

APP_TYPE_LAMBDA = "LAMBDA_SMART_APP"
APP_TYPE_WEBHOOK = "WEBHOOK_SMART_APP"
CLASSIFICATION_AUTOMATION = "AUTOMATION"

_APP_NAME_PATTERN = re.compile('^[a-z0-9._-]{1,250}$', re.IGNORECASE)


class App:
    """Define the app class."""

    def __init__(self, api: API, data: Optional[dict]):
        """Initialize a new instance of the App class."""
        self._api = api
        self._app_name = None
        self._display_name = None
        self._description = None
        self._single_instance = False
        self._app_type = None
        self._classifications = []
        self._lambda_functions = []
        self._webhook_target_url = None
        self._webhook_public_key = None
        self._app_id = None
        self._created_date = None
        self._last_updated_date = None
        if data:
            self.load(data)

    def refresh(self):
        """Refresh the app information using the API."""
        if not self._api:
            raise ValueError("Cannot refresh without an API instance.")
        if not self._app_id:
            raise ValueError("Cannot refresh without an app_id")
        data = self._api.get_app_details(self._app_id)
        self.load(data)

    def load(self, data: dict):
        """Set the states of the app with the supplied data."""
        self._app_name = data['appName']
        self._app_id = data['appId']
        self._app_type = data['appType']
        self._classifications = data['classifications']
        self._display_name = data['displayName']
        self._description = data['description']
        self._created_date = data['createdDate']
        self._last_updated_date = data['lastUpdatedDate']
        self._single_instance = data.get('singleInstance',
                                         self._single_instance)
        if self.app_type == APP_TYPE_WEBHOOK and 'webhookSmartApp' in data:
            self._webhook_target_url = data['webhookSmartApp']['targetUrl']
            self._webhook_public_key = data['webhookSmartApp']['publicKey']
        if self.app_type == APP_TYPE_LAMBDA and 'lambdaSmartApp' in data:
            self._lambda_functions = data['lambdaSmartApp']['functions']

    def save(self):
        """Create the app if it's new, or saves the changes."""
        data = {
            'appName': self._app_name,
            'displayName': self._display_name,
            'description': self._description,
            'singleInstance': self._single_instance,
            'classifications': self._classifications,
            'appType': self._app_type
        }
        if self._app_type == APP_TYPE_WEBHOOK:
            data['webhookSmartApp'] = {
                'targetUrl': self._webhook_target_url
            }
        if self._app_type == APP_TYPE_LAMBDA:
            data['lambdaSmartApp'] = {
                'functions': self._lambda_functions
            }
        # create new app if _app_id is none.
        if not self._app_id:
            response = self._api.create_app(data)
            self.load(response['app'])
            return {
                'oauth_client_id': response['oauthClientId'],
                'oauth_client_secret': response['oauthClientSecret']
            }
        # update existing app
        response = self._api.update_app(self._app_id, data)
        self.load(response)

    def oauth(self) -> OAuthEntity:
        """Get the app's OAuth settings."""
        return OAuthEntity(
            self._api, self._app_id, self._api.get_app_oauth(self._app_id))

    @property
    def app_id(self) -> str:
        """Get the application id."""
        return self._app_id

    @property
    def created_date(self):
        """Get the created date of the app."""
        return self._created_date

    @property
    def last_updated_date(self):
        """Get the last updated date of the app."""
        return self._last_updated_date

    @property
    def app_name(self) -> str:
        """
        Get the app name.

        A globally unique, developer-defined identifier for an app. It is
        alpha-numeric, may contain dashes, underscores, periods, and must
        be less then 250 characters long. ^[a-z0-9.-_]{1,250}$
        """
        return self._app_name

    @app_name.setter
    def app_name(self, value: str):
        """Set the app name."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if not _APP_NAME_PATTERN.match(value):
            raise ValueError("value must be alpha-numeric, may contain dashes "
                             "underscores, periods, and must be less then 250 "
                             "characters long.")
        self._app_name = value

    @property
    def display_name(self) -> str:
        """
        Get the display name.

        A default display name for an app. <= 75 characters
        """
        return self._display_name

    @display_name.setter
    def display_name(self, value: str):
        """Set the display name."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if len(value) > 75:
            raise ValueError("value must be <= 75 characters in length.")
        self._display_name = value

    @property
    def description(self) -> str:
        """
        Get the description.

        A default description for an app. <= 250 characters
        """
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the description."""
        if not value:
            raise ValueError("value cannot be None or zero length.")
        if len(value) > 250:
            raise ValueError("value must be <= 250 characters in length.")
        self._description = value

    @property
    def single_instance(self) -> bool:
        """
        Get the single instance parameter.

        Inform the installation systems that a particular app can only be
        installed once within a user's account.
        """
        return self._single_instance

    @single_instance.setter
    def single_instance(self, value: bool):
        """Set the single instance parameter."""
        self._single_instance = bool(value)

    @property
    def classifications(self) -> List[str]:
        """Get the classifications of the app."""
        return self._classifications

    @property
    def app_type(self) -> str:
        """
        Get the app type.

        Denotes the type of app. "LAMBDA_SMART_APP" "WEBHOOK_SMART_APP"
        """
        return self._app_type

    @app_type.setter
    def app_type(self, value: str):
        """Set the app type."""
        if value not in (APP_TYPE_LAMBDA, APP_TYPE_WEBHOOK):
            raise ValueError("value must be 'LAMBDA_SMART_APP' "
                             "or 'WEBHOOK_SMART_APP'")
        self._app_type = value

    @property
    def lambda_functions(self) -> List[str]:
        """
        Get the list of AWS arns referencing a Lambda function.

        Details related to a Lambda Smart App implementation. This model
        should only be specified for apps of type LAMBDA_SMART_APP.
        """
        return self._lambda_functions

    @property
    def webhook_target_url(self) -> str:
        """Get the URL that should be invoked during execution."""
        return self._webhook_target_url

    @webhook_target_url.setter
    def webhook_target_url(self, value: str):
        """Set the URL that should be invoked during execution."""
        self._webhook_target_url = value

    @property
    def webhook_public_key(self) -> str:
        """Get the public half of an RSA key pair."""
        return self._webhook_public_key
