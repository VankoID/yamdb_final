import uuid

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import EMAIL_HOST_USER

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = CustomUser
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            raise ValidationError("Error! username can't be 'me'!")
        else:
            return CustomUser.objects.create(**validated_data)


class GetMyselfSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = CustomUser
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email')
        model = CustomUser

    def create(self, validated_data):
        check_user = CustomUser.objects.filter(
            username=validated_data['username']).exists()
        if not check_user:
            if validated_data['username'] == 'me':
                raise ValidationError("Error! username can't be 'me'!")
            check_email = CustomUser.objects.filter(
                email=validated_data['email']).exists()
            if check_email:
                raise ValidationError("User with this email is already exists")
            code = str(uuid.uuid4())
            send_mail(
                'Confirmation code',
                code,
                EMAIL_HOST_USER,
                [validated_data['email']],
                fail_silently=False
            )
            CustomUser.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                confirmation_code=code
            )
            return None
        else:
            check_all_fields = CustomUser.objects.filter(
                username=validated_data['username']).filter(
                    email=validated_data['email']).exists()
            if check_all_fields:
                user = CustomUser.objects.get(
                    username=validated_data['username'],
                    email=validated_data['email'])
                send_mail(
                    'Confirmation code',
                    user.confirmation_code,
                    EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return user
            else:
                raise ValidationError(
                    "User with this username is already exists"
                )


class LoginSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = CustomUser
        extra_kwargs = {
            'username': {
                'validators': []
            },
        }
