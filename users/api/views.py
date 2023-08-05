from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet, ViewSet
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import *
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from .response_messages import *
from ..helpers import *

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SignupViewSet(ModelViewSet):
    """
    # Request
    {
        "username":"email",
        "password":"password"
    }
    # 200 Response{
        "token": <auth_token>,
        "user" : user_details,
    }
    """

    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data["id"])
        user_serializer = UserSerializer(user,context={"request":request})
        token, created = Token.objects.get_or_create(user=user)
        data = {"token": token.key, "user": user_serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)

class LoginViewSet(ViewSet):
    """
    # Request
    {
        "username":"email",
        "password":"password"
    }
    # 200 Response if user not verified{
        "status":"ERROR",
        "token": <auth_token>,
        "user" : user_details,
        "message": "otp sended"
    }
    # 200 Response if user verified{
        "token": <auth_token>,
        "user" : user_details
    }
    """
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        if user.is_verified == True:
            return Response(
                {"token": token.key, "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )

        sendOtpEmail(user)
        data = {
            "token": token.key,
            "user": user_serializer.data,
        }

        return Response(data=data, status=status.HTTP_200_OK)

        
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class verifyOtpView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def list(self,request):
        otp = self.request.GET.get("otp", None)
        if otp is None:
            data = {"status": "ERROR", "message": "otp is required for verification"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        verify = verifyOtp(user, otp)
        if verify == True:
            token = Token.objects.get(user=user)
            data = {"status": "OK", "token": token.key, "message": "email verified"}
            return Response(data=data, status=status.HTTP_200_OK)

        data = {"status": "ERROR", "message": "Invalid OTP"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class sendOtpView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def list(self,request):
        user = self.request.user
        sendOtpEmail(user)
        data = {"status": "OK", "message": "OTP is sended to registered email"}
        return Response(data=data, status=status.HTTP_200_OK)


class resetEmailView(ViewSet):
    
    def list(self,request):
        email = self.request.GET.get("email", None)
        if email is None:
            data = {"status": "ERROR", "message": "email is required"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(email=email)
        except:
            data = {"status": "ERROR", "message": "invalid email address"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        sendOtpEmail(user)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "status": "OK",
            "token": token.key,
            "message": "OTP is sended to registered email",
        }
        return Response(data=data, status=status.HTTP_200_OK)



class resetPasswordView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def create(self,request):
        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)

        if password1 is None or password2 is None:
            data = {"status": "ERROR", "message": "password1 and password2 is required"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if password1 != password2:
            data = {
                "status": "ERROR",
                "message": "password1 and password2 should be same",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if len(password1) < 8:
            data = {
                "status": "ERROR",
                "message": "password should be minimum of 8 characters.",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(password1)
        user.save()

        data = {"status": "OK", "message": "Password Reset Successfullly!"}
        return Response(data=data, status=status.HTTP_200_OK)



class userProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class: UserProfileSerializer
    queryset= UserProfile.objects.all()
    http_method_names = ['get','update','delete']
    
    def list(self,request):
        instance = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    def update(self,request):
        try:
            instance = UserProfile.objects.get(user=request.user)
            serializer = self.serializer_class(instance, data=request.data)
        except:
            serializer = self.serializer_class(data=request.data)
            
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        instance = UserProfile.objects.get(user=request.user)
        instance.delete()
        data = {"status": "ok", "message": delete_response}
        return Response(data=data, status=status.HTTP_200_OK)


class deleteUserView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def list(self):
        user = self.request.user
        user.delete()
        data = {"status": "OK", "message": delete_response}
        return Response(data=data, status=status.HTTP_200_OK)
