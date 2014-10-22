from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class TastyApiKeyAuthentication(authentication.TokenAuthentication):
    """
    Use TastyPie's ApiKeyAuthentication scheme with Django Rest Framework.

    The model property can point to either a legacy tastypie.models.ApiKey model
    or you can migrate your API keys to rest_framework.authtoken.models.Token.
    The latter is recommended if you are planning to remove tastypie from your codebase
    entirely.
    """

    model = Token

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'apikey':
            # check for URL parameter authentication
            username = request.GET.get('username')
            key = request.GET.get('api_key')
            if username and key:
                return self.authenticate_credentials(username, key)
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            username, key = auth[1].split(':')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid username token pair')

        return self.authenticate_credentials(username, key)

    def authenticate_credentials(self, username, key):
        try:
            token = self.model.objects.get(user__username=username, key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)

    def authenticate_header(self, request):
        return 'ApiKey'
