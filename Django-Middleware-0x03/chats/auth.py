from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class Authentication(BaseAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)