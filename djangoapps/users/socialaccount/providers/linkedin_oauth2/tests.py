from users.socialaccount.tests import create_oauth2_tests
from users.tests import MockedResponse
from users.socialaccount.providers import registry

from .provider import LinkedInOAuth2Provider


class LinkedInOAuth2Tests(create_oauth2_tests(
        registry.by_id(LinkedInOAuth2Provider.id))):

    def get_mocked_response(self):
        return MockedResponse(200, """
{
  "emailAddress": "raymond.penners@intenct.nl",
  "firstName": "Raymond",
  "id": "ZLARGMFT1M",
  "lastName": "Penners",
  "pictureUrl": "http://m.c.lnkd.licdn.com/mpr/mprx/0_e0hbvSLc",
  "publicProfileUrl": "http://www.linkedin.com/in/intenct"
}
""")
