from users.socialaccount import providers
from users.socialaccount.providers.base import ProviderAccount
from users.socialaccount.providers.oauth2.provider import OAuth2Provider


class DoubanAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('alt')

    def get_avatar_url(self):
        return self.account.extra_data.get('large_avatar')

    def to_str(self):
        dflt = super(DoubanAccount, self).to_str()
        return self.account.extra_data.get('name', dflt)


class DoubanProvider(OAuth2Provider):
    id = 'douban'
    name = 'Douban'
    package = 'users.socialaccount.providers.douban'
    account_class = DoubanAccount

    def extract_uid(self, data):
        return data['id']

    def extract_common_fields(self, data):
        return dict(username=data.get('id'),
                    name=data.get('name'))


providers.registry.register(DoubanProvider)
