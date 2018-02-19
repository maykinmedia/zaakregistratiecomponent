from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from rest_framework.reverse import reverse
from rest_framework_extensions.fields import ResourceUriField

from zaakmagazijn.rgbz.models import (
    Klantcontact, NatuurlijkPersoon, Rol, Status, StatusType, Zaak, ZaakType
)

from .fields import (
    NestedHyperlinkedRelatedField, NestedRequestHyperlinkedRelatedField,
    ParentHyperlinkedRelatedField
)


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                try:
                    ret[field.field_name] = field.to_representation(attribute, instance)
                except TypeError:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret


class RolSerializer(HyperlinkedModelSerializer):
    zaak = serializers.HyperlinkedRelatedField(
        view_name='rest_api:zaken-detail',
        queryset=Zaak.objects.all(),
    )
    betrokkene = NestedHyperlinkedRelatedField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs={"parent_lookup_zaken": "zaak_id"},
        queryset=NatuurlijkPersoon.objects.all(),
    )

    class Meta:
        model = Rol
        fields = (
            'rolomschrijving',
            'rolomschrijving_generiek',
            'roltoelichting',
            'indicatie_machtiging',
            'zaak',
            'betrokkene',
        )


class StatusTypeSerializer(serializers.HyperlinkedModelSerializer):
    zaaktypeidentificatie = serializers.IntegerField(source="zaaktype.zaaktypeidentificatie")
    zaaktypeomschrijving = serializers.CharField(source="zaaktype.zaaktypeomschrijving")
    zaaktypeomschrijving_generiek = serializers.CharField(source="zaaktype.zaaktypeomschrijving_generiek")
    domein = serializers.CharField(source="zaaktype.domein")
    rsin = serializers.CharField(source="zaaktype.rsin")

    class Meta:
        model = StatusType
        fields = (
            'statustypevolgnummer',
            'statustypeomschrijving',
            'statustypeomschrijving_generiek',
            'zaaktypeidentificatie',
            'zaaktypeomschrijving',
            'zaaktypeomschrijving_generiek',
            'domein',
            'rsin',
            # 'toelichting',
            # 'informeren',
            # 'statustekst',
        )


class ZaakSerializer(serializers.HyperlinkedModelSerializer):
    heeft_als_betrokkene = NestedHyperlinkedRelatedField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs={"parent_lookup_zaken": "zaak_id"},
        many=True,
        queryset=NatuurlijkPersoon.objects.all(),
        source='rol_set',
    )
    zaaktype = NestedHyperlinkedRelatedField(
        view_name='rest_api:zaken_zaaktype-detail',
        lookup_kwargs={"parent_lookup_zaak": "pk"},
        queryset=ZaakType.objects.all(),
    )
    rol_set = serializers.HyperlinkedRelatedField(
        view_name='rest_api:rollen-detail',
        many=True,
        queryset=Rol.objects.all(),
    )
    heeft = serializers.SerializerMethodField()

    class Meta:
        model = Zaak
        fields = (
            'url',
            'zaakidentificatie',
            'bronorganisatie',
            'omschrijving',
            'toelichting',
            'registratiedatum',
            'verantwoordelijke_organisatie',
            'einddatum',
            'startdatum',
            'einddatum_gepland',
            'uiterlijke_einddatum_afdoening',
            'resultaatomschrijving',
            'resultaattoelichting',
            'publicatiedatum',
            # 'vertrouwelijkheidaanduiding',
            'archiefnominatie',
            'archiefstatus',
            'archiefactiedatum',
            'betalingsindicatie',
            'laatste_betaaldatum',
            'zaakgeometrie',
            # 'anderZaakobjectZaak',
            # 'gerelateerdeExterneZaak',
            # 'kenmerkenZaak',
            # 'opschortingZaak',
            # 'verlengingZaak',
            'zaaktype',
            # StUF:tijdvakGeldigheid
            # StUF:tijdstipRegistratie
            # StUF:extraElementen
            # StUF:aanvullendeElementen
            # 'historieMaterieel',
            # 'historieFormeel',
            # 'betreft',
            'heeft',
            # 'heeft_als_adviseur',
            # 'heeft_als_behandelaar',
            # 'heeft_als_belanghebbende',
            # 'heeft_als_beslisser',
            'heeft_als_betrokkene',
            # # 'heeft_als_deelzaken',
            # 'heeft_als_initiator',
            # 'heeft_als_klantcontacter',
            # # 'heeft_als_mede_initiator',
            # # 'heeft_als_uitkomst',
            # 'heeft_als_zaakcoordinator',
            # # 'heeft_contact',
            # # 'heeft_relevante_andere',
            # 'is_deelzaak_van',
            # # 'is_relevant_voor',
            'kent',
            'rol_set',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:zaken-detail', 'lookup_field': 'pk'},
        }

    def get_heeft(self, obj):
        statuses = obj.status_set.all()

        links = []
        for status in statuses:
            links.append(reverse('rest_api:zaken_status-detail', kwargs={'parent_lookup_zaak': obj.pk, 'pk': status.pk}, request=self.context.get('request')))
        return links


class NatuurlijkPersoonSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedRequestHyperlinkedRelatedField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs={"parent_lookup_zaken": "parent_lookup_zaken"},
    )
    parent = ParentHyperlinkedRelatedField(
        view_name='rest_api:zaken-detail',
        lookup_field='parent_lookup_zaken',
        lookup_url_kwarg='pk',
    )

    class Meta:
        model = NatuurlijkPersoon
        fields = (
            'url',
            'parent',
            'burgerservicenummer',
            'nummer_ander_natuurlijk_persoon',
            'geslachtsaanduiding',

            # 'geboorte_zaakobject',
            # 'overlijden_zaakobject',
            # 'StUF:tijdvakGeldigheid',
            # 'StUF:tijdstipRegistratie',
            # 'StUF:extraElementen',
            # 'StUF:aanvullendeElementen',
            # 'historieMaterieel',
        )


class ZaakTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedRequestHyperlinkedRelatedField(
        view_name='rest_api:zaken_zaaktype-detail',
        lookup_kwargs={"parent_lookup_zaak": "parent_lookup_zaak"},
    )
    parent = ParentHyperlinkedRelatedField(
        view_name='rest_api:zaken-detail',
        lookup_field='parent_lookup_zaak',
        lookup_url_kwarg='pk',
    )

    class Meta:
        model = ZaakType
        fields = (
            'url',
            'parent',
            'zaaktypeidentificatie',
            'zaaktypeomschrijving',
            'zaaktypeomschrijving_generiek',
            'domein',
            'rsin',
            # 'doel',
            # 'aanleiding',
            'zaakcategorie',
            # 'toelichting',
            'publicatie_indicatie',
            # 'handelingInitiator',
            # 'onderwerp',
            # 'handelingBehandelaar',
            # 'opschortingMogelijk',
            # 'verlengingMogelijk',
            # 'verlengingstermijn',
            # 'trefwoord',
            'vertrouwelijk_aanduiding',
            'publicatietekst',
            # 'verantwoordelijke',
            # 'publicatie',
            # 'verantwoordingsrelatie',
            # 'versiedatum',
        )

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs.get('context').get('kwargs')
        super().__init__(*args, **kwargs)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedRequestHyperlinkedRelatedField(
        view_name='rest_api:zaken_status-detail',
        lookup_kwargs={"parent_lookup_zaak": "parent_lookup_zaak"},
    )
    parent = ParentHyperlinkedRelatedField(
        view_name='rest_api:zaken-detail',
        lookup_field='parent_lookup_zaak',
        lookup_url_kwarg='pk',
    )
    rol = serializers.HyperlinkedRelatedField(
        view_name='rest_api:rollen-detail',
        queryset=Rol.objects.all(),
    )
    status_type = serializers.HyperlinkedRelatedField(
        view_name='rest_api:statustypen-detail',
        queryset=StatusType.objects.all(),
    )

    class Meta:
        model = Status
        fields = (
            'url',
            'parent',
            'statustoelichting',
            'datum_status_gezet',
            'indicatie_laatst_gezette_status',
            'status_type',
            # 'historieMaterieel',
            # 'historieFormeel',
            # 'heeftRelevant',
            # 'isGezetDoor',
            # 'isVan',
            # 'StUF:tijdvakGeldigheid',
            # 'StUF:tijdstipRegistratie',
            # 'StUF:extraElementen',
            # 'StUF:aanvullendeElementen',
            'rol',
        )


class KlantcontactSerializer(HyperlinkedModelSerializer):
    zaak = serializers.HyperlinkedRelatedField(
        view_name='rest_api:zaken-detail',
        queryset=Zaak.objects.all(),
    )
    natuurlijk_persoon = NestedHyperlinkedRelatedField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs={
            "parent_lookup_zaken": "zaak_id",
        },
        queryset=NatuurlijkPersoon.objects.all(),
    )

    class Meta:
        model = Klantcontact
        fields = (
            'url',
            'identificatie',
            'datumtijd',
            'kanaal',
            'onderwerp',
            'toelichting',
            'zaak',
            'natuurlijk_persoon',
            # 'vestiging', # Heeft nog geen viewset kan niet linken
            # 'medewerker', # Heeft nog geen viewset kan niet linken
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:klantcontact-detail', 'lookup_field': 'pk'},
        }
