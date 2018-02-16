from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from zaakmagazijn.rgbz.models import (
    NatuurlijkPersoon, Rol, Status, StatusType, Zaak, ZaakType
)

from .serializers import (
    NatuurlijkPersoonSerializer, RolSerializer, StatusSerializer,
    StatusTypeSerializer, ZaakSerializer, ZaakTypeSerializer
)


class NestedWithRequestMixin(object):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(kwargs=self.kwargs)
        self.request.kwargs = self.kwargs
        return context


class ZaakViewSet(NestedWithRequestMixin, NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaken' to be viewed or edited.
    """
    queryset = Zaak.objects.all()
    serializer_class = ZaakSerializer


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'rollen' to be viewed or edited.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class StatusTypeViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    '''
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer


class NatuurlijkPersoonViewSet(NestedWithRequestMixin, NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'natuurlijkpersonen' to be viewed or edited.
    """
    queryset = NatuurlijkPersoon.objects.all().distinct()
    serializer_class = NatuurlijkPersoonSerializer


class ZaakTypeViewSet(NestedWithRequestMixin, NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaaktypes' to be viewed or edited.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer


class StatusViewSet(NestedWithRequestMixin, NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaaktypes' to be viewed or edited.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
