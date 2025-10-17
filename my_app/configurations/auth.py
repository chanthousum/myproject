from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import requests
class   KeycloakOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)
        user.email = claims.get("email", "")
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def verify_token(self, token):
        """
        Verify JWT from Keycloak (for API requests)
        """
        from django.conf import settings
        try:
            jwks_url = settings.OIDC_OP_JWKS_ENDPOINT
            jwks_data = requests.get(jwks_url).json()
            unverified_header = jwt.get_unverified_header(token)

            key = next(
                (k for k in jwks_data["keys"] if k["kid"] == unverified_header["kid"]),
                None
            )
            if key is None:
                raise JWTError("Invalid token header: key not found")

            return jwt.decode(
                token,
                key,
                algorithms=[settings.OIDC_RP_SIGN_ALGO],
                audience=settings.KEYCLOAK_AUDIENCE,
                issuer=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}",
            )
        except ExpiredSignatureError:
            raise JWTError("Token has expired")
        except JWTError as e:
            raise JWTError(f"Invalid token: {e}")
