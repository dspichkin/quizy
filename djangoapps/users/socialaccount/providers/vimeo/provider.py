from users.socialaccount import providers
from users.socialaccount.providers.base import ProviderAccount
from users.socialaccount.providers.oauth.provider import OAuthProvider


class VimeoAccount(ProviderAccount):
    pass


class VimeoProvider(OAuthProvider):
    id = 'vimeo'
    name = 'Vimeo'
    package = 'users.socialaccount.providers.vimeo'
    account_class = VimeoAccount

    def get_default_scope(self):
        scope = []
        return scope

    def extract_uid(self, data):
        return data['id']

    def extract_common_fields(self, data):
        return dict(name=data.get('display_name'),
                    username=data.get('username'))


providers.registry.register(VimeoProvider)
