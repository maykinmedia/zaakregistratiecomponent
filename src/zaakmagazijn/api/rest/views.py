from rest_framework import viewsets

from ...rgbz.models import (
    InformatieObject, Klantcontact, Medewerker, NatuurlijkPersoon,
    NietNatuurlijkPersoon, OrganisatorischeEenheid, Rol, Status, StatusType,
    Vestiging, Zaak, ZaakType
)
from .serializers import (
    BetrokkeneSerializer, InformatieObjectSerializer, KlantcontactSerializer,
    MedewerkerSerializer, NatuurlijkPersoonSerializer,
    NietNatuurlijkPersoonSerializer, OrganisatorischeEenheidSerializer,
    RolSerializer, StatusSerializer, StatusTypeSerializer, VestigingSerializer,
    ZaakSerializer, ZaakTypeSerializer
)
from .utils.viewsets import NestedViewSetMixin


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


class NietNatuurlijkPersoonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NietNatuurlijkPersoon.objects.all()
    serializer_class = NietNatuurlijkPersoonSerializer


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vestiging.objects.all()
    serializer_class = VestigingSerializer


class OrganisatorischeEenheidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrganisatorischeEenheid.objects.all()
    serializer_class = OrganisatorischeEenheidSerializer


class BetrokkeneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get the betrokkene information for a role.
    """
    queryset = Rol.objects.all()
    serializer_class = BetrokkeneSerializer
