from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from allauth.account.views import confirm_email
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import TokenProxy
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from django_celery_beat.models import ClockedSchedule, SolarSchedule, IntervalSchedule
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.site_header = "kapoorsoftwaresolutions"
admin.site.site_title = "kapoorsoftwaresolutions Admin Portal"
admin.site.index_title = "kapoorsoftwaresolutions Admin"

admin.site.unregister(EmailAddress)
admin.site.unregister(TokenProxy)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(Site)
admin.site.unregister(Group)

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("kapoorsoftwaresolutions.api_router")),
    path("users/", include("users.urls")),
    path("rest-auth/", include("dj_rest_auth.urls")),
    # Override email confirm to use allauth's HTML view instead of rest_auth's API vi
    path("rest-auth/registration/account-confirm-email/<str:key>/", confirm_email),
    path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]

# swagger
api_info = openapi.Info(
    title="kapoorsoftwaresolutions API",
    default_version="v1",
    description="API documentation for kapoorsoftwaresolutions App",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(),
)

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]


urlpatterns += [path("", TemplateView.as_view(template_name="index.html"))]
urlpatterns += [
    re_path(r"^(?:.*)/?$", TemplateView.as_view(template_name="index.html"))
]
