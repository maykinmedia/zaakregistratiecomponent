from django.utils.translation import ugettext_lazy as _

from rest_framework import authentication
from rest_framework import exceptions

from .models import Organisation


class HeaderAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        organization_name = request.META.get('HTTP_X_NLX_ORGANISATION_CN')
        if not organization_name:
            return None

        try:
            organization = Organisation.objects.get(name=organization_name)
        except Organisation.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('No such organization'))

        return (organization, None)
