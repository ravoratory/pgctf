from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import PGritProvider

urlpatterns = default_urlpatterns(PGritProvider)
