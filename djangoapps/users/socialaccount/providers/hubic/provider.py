from users.socialaccount import providers
from users.socialaccount.providers.base import ProviderAccount
from users.socialaccount.providers.oauth2.provider import OAuth2Provider


class HubicAccount(ProviderAccount):
    pass


class HubicProvider(OAuth2Provider):
    id = 'hubic'
    name = 'Hubic'
    package = 'users.socialaccount.providers.hubic'
    account_class = HubicAccount

    def extract_uid(self, data):
        return str(data['email'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    username=data.get('firstname').lower()+data.get('lastname').lower(),
                    first_name=data.get('firstname'),
                    last_name=data.get('lastname'))

providers.registry.register(HubicProvider)
