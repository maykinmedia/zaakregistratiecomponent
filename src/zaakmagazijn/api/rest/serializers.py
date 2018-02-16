from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_extensions.fields import ResourceUriField

from zaakmagazijn.rgbz.models import (
    NatuurlijkPersoon, Rol, Status, StatusType, Zaak, ZaakType
)

from .fields import (
    NestedHyperlinkedIdentityField, NestedRequestHyperlinkedIdentityField,
    ParentHyperlinkedIdentityField
)


class RolSerializer(serializers.HyperlinkedModelSerializer):
    zaak = serializers.HyperlinkedIdentityField(
        view_name='rest_api:zaken-detail',
    )
    betrokkene = NestedHyperlinkedIdentityField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_field='betrokkene_id',
        lookup_url_kwarg='pk',
        lookup_kwargs={
            "parent_lookup_zaken": "zaak_id",
        },
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
    heeft_als_betrokkene = NestedHyperlinkedIdentityField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_field='betrokkene_id',
        lookup_url_kwarg='pk',
        lookup_kwargs={
            "parent_lookup_zaken": "zaak_id",
        },
        many=True,
        source='rol_set',
    )
    zaaktype = NestedHyperlinkedIdentityField(
        view_name='rest_api:zaken_zaaktype-detail',
        lookup_field='zaaktype_id',
        lookup_url_kwarg='pk',
        lookup_kwargs={
            "parent_lookup_zaak": "pk",
        },
    )
    rol_set = serializers.HyperlinkedIdentityField(
        view_name='rest_api:rollen-detail',
        many=True,
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
    url = NestedRequestHyperlinkedIdentityField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs={
            "parent_lookup_zaken": "parent_lookup_zaken"
        },
    )
    parent = ParentHyperlinkedIdentityField(
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

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs.get('context').get('kwargs')
        super().__init__(*args, **kwargs)


class ZaakTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedRequestHyperlinkedIdentityField(
        view_name='rest_api:zaken_zaaktype-detail',
        lookup_kwargs={
            "parent_lookup_zaak": "parent_lookup_zaak"
        },
    )
    parent = ParentHyperlinkedIdentityField(
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
    url = NestedRequestHyperlinkedIdentityField(
        view_name='rest_api:zaken_status-detail',
        lookup_kwargs={
            "parent_lookup_zaak": "parent_lookup_zaak"
        },
    )
    parent = ParentHyperlinkedIdentityField(
        view_name='rest_api:zaken-detail',
        lookup_field='parent_lookup_zaak',
        lookup_url_kwarg='pk',
    )
    rol = serializers.HyperlinkedIdentityField(
        view_name='rest_api:rollen-detail',
        lookup_field='rol_id',
        lookup_url_kwarg='pk',
    )
    status_type = serializers.HyperlinkedIdentityField(
        view_name='rest_api:statustypen-detail',
        lookup_field='status_type_id',
        lookup_url_kwarg='pk',
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
