from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.api.views import (
    UserViewSet,
    SignupViewSet,
    LoginViewSet,
    verifyOtpView,
    sendOtpView,
    resetEmailView,
    resetPasswordView,
    userProfileView,
    deleteUserView,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("verify-otp", verifyOtpView, basename="verify-otp")
router.register("send-otp", sendOtpView, basename="send-otp")
router.register("reset-email", resetEmailView, basename="reset-email")
router.register("reset-password", resetPasswordView, basename="reset-password")
router.register("user-profile", userProfileView, basename="user-profile")
router.register("delete-user", deleteUserView, basename="delete-user")



app_name = "api"
urlpatterns = router.urls
