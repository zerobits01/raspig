from typing import Any, Tuple

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class ExpiringTokenAuthentication(TokenAuthentication):
    def __init__(self) -> None:
        self.request = None

    def authenticate(self, request: Request):
        self.request = request
        return super(ExpiringTokenAuthentication, self).authenticate(request)

    def authenticate_credentials(self, key: str) -> Tuple[Any, str]:
        return_value = super(ExpiringTokenAuthentication,
                             self).authenticate_credentials(key)

        token = Token.objects.get(key=key)
        if (timezone.now() - token.created).total_seconds() / 60 > 15:
            token.delete()
            raise AuthenticationFailed('Token has expired')
        # TODO If notifications were polling don't update token create time
        token.created= timezone.now()
        token.save()
        return return_value
