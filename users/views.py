from rest_framework import viewsets, mixins, status, generics
from .models import User, SecretToken, SendEmail, Favorite
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotFound
from drf_yasg.utils import swagger_auto_schema
from . import messages
from rest_framework.decorators import action

# Create your views here.


class SignUpView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.SignUpSerializer
    permission_classes = ()


class SignInView(APIView):

    serializer_class = serializers.SignInSerializer
    permission_classes = ()
    throttle_scope = 'login'

    @swagger_auto_schema(request_body=serializers.SignInSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = user.get_token()

        return Response(
            {
                'token': token,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_patient': user.is_patient,
                'is_doctor': user.is_doctor,
            },
            status=status.HTTP_200_OK
        )


class EmailVerificationView(APIView):

    permission_classes = ()

    def get_token(self):
        key = self.request.GET.get('token')
        token = SecretToken.objects.filter(key=key).first()

        if token is None:
            raise NotFound({
                'error': 'token is invalid'
            })

        if token.is_expired:
            raise ValidationError({
                'error': 'token is expired'
            })
        return token

    def get_user(self):
        token = self.get_token()
        user = User.objects.filter(id=token.user.id).first()

        if user.is_active:
            raise ValidationError({
                'message': 'your account is already activated'
            })
        return user

    def get(self, request):
        token = self.get_token()
        user = self.get_user()

        user.activate()
        token.deactivate()

        # send sucess verification email
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=messages.SUCCESS_ACTIVATION_SUBJECT,
            message=messages.SUCCESS_ACTIVATION_MESSAGE
        )
        return Response(
            {
                'message': 'You are active now'
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordView(generics.CreateAPIView):

    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = ()
    throttle_scope = 'reset_password'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        SendEmail.objects.create(
            email_type='RESET_PASSWORD',
            email=user.email
        )
        return Response(
            {
                'message': 'Check your email for Reset Password'
            },
            status=status.HTTP_200_OK
        )


class ConfirmResetPasswordView(generics.CreateAPIView):

    serializer_class = serializers.ConfirmResetPassword

    def get_token(self):
        key = self.request.GET.get('token', '')
        token = SecretToken.objects.filter(key=key).first()

        if token is None:
            raise NotFound({
                'error': 'token is invalid'
            })

        if token.is_expired:
            raise ValidationError({
                'error': 'token is expired'
            })
        return token

    def get_user(self):
        token = self.get_token()
        user = User.objects.filter(id=token.user.id).first()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.get_token()
        user = self.get_user()
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        token.deactivate()

        # send sucess reset password
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=messages.SUCCESS_RESET_PASSWORD_SUBJECT,
            message=messages.SUCCESS_RESET_PASSWORD_MESSAGE
        )
        return Response(
            {
                'message': 'Password is reset successfully'
            },
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):

    serializer_class = serializers.ChangePasswordSerializer

    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer)
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        # send sucess change password
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=messages.SUCCESS_CHANGE_PASSWORD_SUBJECT,
            message=messages.SUCCESS_CHANGE_PASSWORD_MESSAGE
        )
        return Response(
            {
                'message': 'Password changed Successfully'
            }
        )


class LogoutView(APIView):

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {
                'message': 'Logout Successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class ResendEmailVerificationView(APIView):

    serializer_class = serializers.ResendEmailVerificationSerializer
    permission_classes = ()
    throttle_scope = 'resend_verification'

    @swagger_auto_schema(request_body=serializers.ResendEmailVerificationSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Check your email'
            },
            status=status.HTTP_200_OK
        )


class ProfileView(viewsets.GenericViewSet, generics.UpdateAPIView):

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, many=False)
        return Response(
            {
                'code': 'SUCCESS',
                'data': serializer.data
            }
        )

    @action(methods=['GET'], detail=False)
    def favorites(self, *args, **kwargs):
        user = self.get_object()
        favourit = Favorite.objects.prefetch_related(
            'items'
        ).filter(user=user).first()
        serializer = serializers.FavoriteSerializer(favourit)
        return Response(
            {
                'code': 'SUCCESS',
                'data': serializer.data
            }
        )
