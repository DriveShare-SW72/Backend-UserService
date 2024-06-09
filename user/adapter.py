from allauth.account.utils import messages
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        messages.error(request, "external provider canceled", extra_tags="error")
        raise ImmediateHttpResponse(response=redirect('home'))
        return super().on_authentication_error(request, provider, error, exception, extra_context)
