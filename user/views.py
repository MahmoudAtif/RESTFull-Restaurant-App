from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from .send_emails import send_email
from django.contrib.auth.models import User
from django.urls import reverse
from .throttlings import CustomeResetPassswordThruttle
from .models import Customer


# Create your views here.

class SignInView(APIView):
    
    permission_classes=()
    throttle_classes=()

    def get(self, request):
        response = {
            'messsage':'Enter (email or username) and password for login' 
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.SignInSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token':token.key
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpView(APIView):
    
    permission_classes=()
    throttle_classes=()

    def get(self, request):
        response = {
            'messsage':'Enter data for registeration' 
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            user = User.objects.get(username=data['username'])
            token = Token.objects.get(user=user)
            current_site=get_current_site(request)
            message = f'Go to Link to Verify Your account {current_site.domain}/user/email-verification/?token={token.key}'
            send_email('Successfully Registeration', message, data['email'])
            response = [serializer.data, {
                'Registeration successfully check you email for activation'
            }]
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    
    throttle_classes=()
    permission_classes=()

    def get_user(self,token):
        try:
            user_token = Token.objects.get(key=token)
            return user_token.user
        except:
            return None

    def get(self, request):
        token = request.GET.get('token')
        user = self.get_user(token)
        user.is_active=True
        user.save()
        response = {
            'messsage':'Success verification, you are active now' 
        }
        return Response(response, status=status.HTTP_200_OK) 

class ChangePasswordView(APIView):

    def get_object(self, request):
        obj = request.user
        return obj
    
    def get(self, request):
        response = {
            'messsage':'Enter old password and new password' 
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object(request)
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['new_password'])
                user.save()
                response = {
                    'message':'Password change successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'error':'old password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    
    permission_classes=()
    throttle_classes = (CustomeResetPassswordThruttle,)
    
    def get(self, request):
        response = {
            'messsage':'Enter email address to reset your password' 
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.get(email=request.data['email'])
            token=Token.objects.get(user=user)
            current_site=get_current_site(request)
            message = f'Go to Link to Reset Password {current_site.domain}/user/confirm-password/?token={token.key}'
            send_email('Reset Password', message, request.data['email'])
            response = [serializer.data, {
                'message':'Check you email to reset password'
            }]
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordConfirmView(APIView):
    
    permission_classes = ()
    throttle_classes = ()
    
    def get_user(self, token): 
        token = Token.objects.get(key=token)
        return token.user

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            response = {
                'error':'not exist any token'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST    )
        response = {
            'token':token
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.PasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = request.GET.get('token')
            user = self.get_user(token)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            response = {
                'message':'Password Reset Done'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomersView(viewsets.ModelViewSet):
    permission_classes=()
    throttle_classes=()
    queryset = Customer.objects.all()
    serializer_class=serializers.CustomerSerializer
