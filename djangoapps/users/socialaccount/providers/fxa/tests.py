from users.socialaccount.tests import create_oauth2_tests
from users.tests import MockedResponse
from users.socialaccount.providers import registry

from .provider import FirefoxAccountsProvider


class FirefoxAccountsTests(create_oauth2_tests(registry.by_id(FirefoxAccountsProvider.id))):
    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "uid":"6d940dd41e636cc156074109b8092f96",
            "email":"user@example.domain"
        }""")
