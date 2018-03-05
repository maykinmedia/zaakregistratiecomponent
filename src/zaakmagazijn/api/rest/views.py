from rest_framework import viewsets

from .utils.viewsets import NestedViewSetMixin
from ...rgbz.models import (
    InformatieObject, Klantcontact, Medewerker, NatuurlijkPersoon, Rol, Status,
    StatusType, Zaak, ZaakType)
from .serializers import (
    InformatieObjectSerializer, KlantcontactSerializer, MedewerkerSerializer,
    NatuurlijkPersoonSerializer, RolSerializer, StatusSerializer,
    StatusTypeSerializer, ZaakSerializer, ZaakTypeSerializer)

class ZaakViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaken' to be viewed.
    """
    queryset = Zaak.objects.all()
    serializer_class = ZaakSerializer


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'rollen' to be viewed.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class StatusTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'statustypes' to be viewed.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer


class NatuurlijkPersoonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'natuurlijkpersonen' to be viewed.
    """
    queryset = NatuurlijkPersoon.objects.all().distinct()
    serializer_class = NatuurlijkPersoonSerializer


class ZaakTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaaktypes' to be viewed.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer


class StatusViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'zaaktypes' to be viewed.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class KlantcontactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows 'klantcontact' to be viewed or edited.
    """
    queryset = Klantcontact.objects.all()
    serializer_class = KlantcontactSerializer


class MedewerkerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'medewerker' to be viewed.
    """
    queryset = Medewerker.objects.all()
    serializer_class = MedewerkerSerializer


class InformatieObjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows 'informatieobject' to be viewed.
    """
    queryset = InformatieObject.objects.all()
    serializer_class = InformatieObjectSerializer
