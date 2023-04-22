from restaurant.serializers import MenuItemSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, SendEmail, Favorite
from django.db import transaction
from rest_framework.exceptions import NotFound


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'first_name': {
                'required': False,
                'read_only': True
            },
            'last_name': {
                'required': False,
                'read_only': True
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.deactivate()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({
                "error": "password didn't match !!"
            })

        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['message'] = 'Check your Email for Verification'
        representation['token'] = instance.get_token()
        return representation


class SignInSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']
        user = authenticate(username=email_username, password=password)

        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        'error': 'Your acoount is disable',
                        'status': 'User inactive',
                    }
                )
        else:
            raise serializers.ValidationError(
                {
                    'error': 'unable to login with provided credential',
                }
            )

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise NotFound({
                'error': 'No account was found with this email'
            })

        attrs['user'] = user
        return attrs


class ConfirmResetPassword(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError({
                "error": "password didn't match!!"
            })
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context.get('request', None).user

        if not user.check_password(value):
            raise serializers.ValidationError('password is wrong')

        return value


class ResendEmailVerificationSerializer(serializers.Serializer):

    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']
        user = authenticate(username=email_username, password=password)

        if user is None:
            raise serializers.ValidationError(
                {
                    'error': 'unable to access with provided credential'
                }
            )

        if user.is_active:
            raise serializers.ValidationError(
                {
                    'error': 'this account is already activated'
                }
            )

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        obj = SendEmail.objects.create(
            email_type='EMAIL_VERIFICATION',
            email=user.email
        )
        return obj


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'email': {
                'read_only': True
            },
            'first_name': {
                'required': False
            },
            'last_name': {
                'required': False
            },
        }


class FavoriteSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(read_only=True, many=True)

    class Meta:
        model = Favorite
        exclude = ['user']
