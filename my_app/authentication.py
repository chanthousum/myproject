from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
from my_app.auth import KeycloakOIDCBackend

class KeycloakJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        backend = KeycloakOIDCBackend()
        try:
            claims = backend.verify_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        user, _ = User.objects.get_or_create(username=claims.get("preferred_username"))
        return (user, None)
