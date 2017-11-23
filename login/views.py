from login.models import Account
from django.contrib.auth import authenticate, login, logout
from login.serializers import AccountSerializer
from rest_framework import status, views, permissions, viewsets
from rest_framework.response import Response
import json

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    lookup_field = 'username'
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)
        account = authenticate(username = username, password = password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account, context={'request': request})
                return Response(serialized.data)
            else:
                return Response({
                        'status': 'Unauthorized',
                        'message': 'This account has been disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
                return Response({
                        'status': 'Unauthorized',
                        'message': 'Username/Password combination invalid.'
                    }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,) # remove comma?

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
