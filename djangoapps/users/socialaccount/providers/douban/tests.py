from users.socialaccount.tests import create_oauth2_tests
from users.tests import MockedResponse
from users.socialaccount.providers import registry

from .provider import DoubanProvider


class DoubanTests(create_oauth2_tests(registry.by_id(DoubanProvider.id))):
    def get_mocked_response(self):
        return MockedResponse(200, """
            {"name": "guoqiao",
             "created": "2009-02-18 01:07:52",
             "is_suicide": false,
             "alt": "http://www.douban.com/people/qguo/",
             "avatar": "http://img3.douban.com/icon/u3659811-3.jpg",
             "signature": "",
             "uid": "qguo",
             "is_banned": false,
             "desc": "\u4e0d\u662f\u5f88\u7231\u8bfb\u4e66",
             "type": "user",
             "id": "3659811",
             "large_avatar": "http://img3.douban.com/icon/up3659811-3.jpg"}
""")