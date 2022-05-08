from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView



from auth_app.utils import ExpiringTokenAuthentication


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request: Request) -> Response:
        try:
            return_response = super(ObtainExpiringAuthToken, self).post(request)
            token = Token.objects.get(key=return_response.data['token'])
            token.created = timezone.now()
            token.save()
            return Response({'token': return_response.data.get('token'), 'user': str(token.user)})
        except Exception as e:
            return Response({'errors': ['authentication failed']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class Ping(APIView):
    def get(self, request: Request) -> Response:
        return Response('pong', status=status.HTTP_200_OK)


class ChangePassword(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> HttpResponse:
        try:
            password = request.data['password']
            request.user.set_password(str(password))
            request.user.save()
            return HttpResponse(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors': ['couldn\'t change password']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> HttpResponse:
        Token.objects.filter(key=request.auth).delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
