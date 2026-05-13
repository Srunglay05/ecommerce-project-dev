from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import AccessToken

class QueryParamAccessTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            return None  # No token passed

        try:
            access_token = AccessToken.objects.get(token=token, is_active=True)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive token")

        # Return a user object if your AccessToken is linked to one, or None
        return (None, None)  # or (access_token.user, access_token) if user-linked
