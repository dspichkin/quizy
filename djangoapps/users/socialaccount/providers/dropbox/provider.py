from users.socialaccount import providers
from users.socialaccount.providers.base import ProviderAccount
from users.socialaccount.providers.oauth.provider import OAuthProvider


class DropboxAccount(ProviderAccount):
    pass


class DropboxProvider(OAuthProvider):
    id = 'dropbox'
    name = 'Dropbox'
    package = 'users.socialaccount.providers.dropbox'
    account_class = DropboxAccount

    def extract_uid(self, data):
        return data['uid']

    def extract_common_fields(self, data):
        return dict(username=data.get('display_name'),
                    name=data.get('display_name'),
                    email=data.get('email'))

providers.registry.register(DropboxProvider)
