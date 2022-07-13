import json

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2CallbackView, OAuth2LoginView

from .provider import PGritProvider


class PGritAPI(OAuth2Client):
    """
    verify my account credendiatls.
    """
    url = 'https://community.4nonome.com/api/v1/accounts/verify_credentials'

    def get_user_info(self):
        user = json.loads(self.query(self.url))
        return user

class PGritOAuth2Adapter(OAuth2Adapter):
    provider_id = PGritProvider.id
    request_token_url = 'https://community.4nonome.com/api/v1/apps'
    access_token_url = 'https://community.4nonome.com/oauth/token'
    authorize_url = 'https://community.4nonome.com/oauth/authorize'
    
    def complete_login(self, request, app, access_token, **kwargs):
        client = PGritAPI(request, app.client_id, app.secret, self.request_token_url)
        
        extra_data = client.get_user_info()
        return self.get_provider().sociallogin_from_response(request, extra_data)
    
    def get_login_redirect_url(self, request):
        return "urn:ietf:wg:oauth:2.0:oob"
    

oauth2_login = OAuth2LoginView.adapter_view(PGritOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(PGritOAuth2Adapter)
