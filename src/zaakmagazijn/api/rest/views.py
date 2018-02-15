from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from zaakmagazijn.rgbz.models.betrokkene import NatuurlijkPersoon, Rol
from zaakmagazijn.rgbz.models.zaken import Zaak

from .serializers import (
    NatuurlijkPersoonSerializer, RolSerializer, ZaakSerializer
)


class ZaakViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows 'zaken' to be viewed or edited.
    """
    queryset = Zaak.objects.all()
    serializer_class = ZaakSerializer


class RolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows 'rollen' to be viewed or edited.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class NatuurlijkPersoonViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows 'natuurlijkpersonen' to be viewed or edited.
    """
    queryset = NatuurlijkPersoon.objects.all()
    serializer_class = NatuurlijkPersoonSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(kwargs=self.kwargs)
        self.request.fewefwew = self.kwargs
        return context
