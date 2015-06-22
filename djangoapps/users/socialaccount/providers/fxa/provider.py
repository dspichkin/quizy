from users.socialaccount import providers
from users.socialaccount.providers.base import ProviderAccount
from users.socialaccount.providers.oauth2.provider import OAuth2Provider


class FirefoxAccountsAccount(ProviderAccount):

    def to_str(self):
        return self.account.uid


class FirefoxAccountsProvider(OAuth2Provider):
    id = 'fxa'
    name = 'Firefox Accounts'
    package = 'users.socialaccount.providers.fxa'
    account_class = FirefoxAccountsAccount

    def get_default_scope(self):
        return ['profile']

    def extract_uid(self, data):
        return str(data['uid'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'))


providers.registry.register(FirefoxAccountsProvider)
