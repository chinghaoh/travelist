from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from .models import APIKey

class APIKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'users.auth.APIKeyAuthentication'
    name = 'ApiKeyAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter: Api-Key 97286785-b318-44a9-9387-0fc83c2b4ba4, to test the demo',
        }

class APIKeyAuthentication(BaseAuthentication):
    keyword = 'Api-Key'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith(self.keyword + ' '):
            return None

        raw_key = auth_header[len(self.keyword) + 1:].strip()

        try:
            api_key = APIKey.objects.select_related('user').get(key=raw_key, is_active=True)
        except (APIKey.DoesNotExist, ValueError):
            raise AuthenticationFailed('Invalid or revoked API key.')

        APIKey.objects.filter(pk=api_key.pk).update(last_used_at=timezone.now())

        return (api_key.user, api_key)

    def authenticate_header(self, request):
        return self.keyword