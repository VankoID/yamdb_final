import uuid

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .permissions import AdminOnly
from .serializers import (GetMyselfSerializer, LoginSerializer,
                          SignupSerializer, UserSerializer)


class SignUpViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdminOnly,)

    def perform_create(self, serializer):
        code = str(uuid.uuid4())
        serializer.save(confirmation_code=code)

    @action(methods=['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=(IsAuthenticated,))
    def get_myself(self, request):
        user = self.request.user
        instance = get_object_or_404(CustomUser, username=user.username)
        if request.method == 'GET':
            seriaizer = GetMyselfSerializer(instance=instance)
            return Response(seriaizer.data)
        serializer = GetMyselfSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }


class GetTokenView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = CustomUser.objects.filter(
            username=serializer.data['username']).exists()
        if check:
            check_code = CustomUser.objects.filter(
                username=serializer.data['username'],
                confirmation_code=serializer.data['confirmation_code']
            ).exists()
            if check_code:
                user = get_object_or_404(
                    CustomUser,
                    username=serializer.data['username'],
                    confirmation_code=serializer.data['confirmation_code'])
                return Response(get_tokens_for_user(user))
            else:
                return Response(
                    'Confirmation code incorrect',
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                'User does not exists',
                status=status.HTTP_404_NOT_FOUND)
