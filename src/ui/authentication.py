from rest_framework.authentication import TokenAuthentication

# Create your views here.


class TokenAuthSupportCookie(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support cookie based authentication
    """

    def authenticate(self, request):
        # Check if 'auth_token' is in the request cookies.
        # Give precedence to 'Authorization' header.
        if 'auth_token' in request.COOKIES and \
                'HTTP_AUTHORIZATION' not in request.META:
            print(request.COOKIES.get('auth_token'))
            return self.authenticate_credentials(
                request.COOKIES.get('auth_token')
            )
        return super().authenticate(request)