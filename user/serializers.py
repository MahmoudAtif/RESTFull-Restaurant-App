from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .backends import EmailBackEnd
from rest_framework.authtoken.models import Token
from .models import Customer

class SignInSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email = attrs['username_or_email']
        password = attrs['password']

        if username_or_email and password:
            user = EmailBackEnd.authenticate(username=username_or_email, password=password)
            if user is not None:
                if not user.is_active:
                   raise serializers.ValidationError({
                    'status':'error',
                    'msg':'You must activate Your email address'
                   }) 
            else:    
                raise serializers.ValidationError({
                    'status':'error',
                    'msg':'unable to login with provided credential'
                })
        else:
            raise serializers.ValidationError({
                'status':'error',
                'msg':'username and password must be not empty'
            })
        attrs['user']=user
        return attrs




class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','is_active']     

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        password = validated_data.pop('password',None)
        if password is not None:
            user.is_active=False
            user.set_password(password)
            user.save()
            return user

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('email address already used')
        return super().validate(attrs)



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exist = User.objects.filter(email=attrs['email']).exists()
        if not email_exist:
            raise serializers.ValidationError({
                'status':'error',
                'msg':'email address not provided for any user'
            })
        return super().validate(attrs)

class PasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        token=attrs['token']
        token_exists = Token.objects.filter(key=token).exists()
        if not token_exists:
            raise serializers.ValidationError({
                'status':'error',
                'msg':'Token is not valid'
            })
        return super().validate(attrs)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields='__all__'