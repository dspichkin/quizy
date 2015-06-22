# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.socialaccount.tests import create_oauth_tests
from users.tests import MockedResponse
from users.socialaccount.providers import registry

from .provider import DropboxProvider


class DropboxTests(create_oauth_tests(registry.by_id(DropboxProvider.id))):
    def get_mocked_response(self):
        # FIXME: Replace with actual/complete Dropbox response
        return [MockedResponse(200, """
    { "uid": "123" }
""")]
