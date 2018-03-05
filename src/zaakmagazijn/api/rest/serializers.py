from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...rgbz.models import (
    InformatieObject, Klantcontact, Medewerker, NatuurlijkPersoon, Rol, Status,
    StatusType, Zaak, ZaakType,
    Betrokkene)

class RolSerializer(serializers.HyperlinkedModelSerializer):
    betrokkene = serializers.HyperlinkedRelatedField(
        read_only=True,
        source='betrokkene.object_ptr',
        view_name='rest_api:natuurlijke-personen-detail',
    )

    class Meta:
        model = Rol
        fields = (
            'url',
            'rolomschrijving',
            'rolomschrijving_generiek',
            'roltoelichting',
            'indicatie_machtiging',
            'zaak',
            'betrokkene',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:rollen-detail'},
            'zaak': {'view_name': 'rest_api:zaken-detail'},
        }


class StatusTypeSerializer(serializers.HyperlinkedModelSerializer):
    zaaktypeidentificatie = serializers.IntegerField(source='zaaktype.zaaktypeidentificatie', read_only=True)
    zaaktypeomschrijving = serializers.CharField(source='zaaktype.zaaktypeomschrijving', read_only=True)
    zaaktypeomschrijving_generiek = serializers.CharField(source='zaaktype.zaaktypeomschrijving_generiek', read_only=True)
    domein = serializers.CharField(source='zaaktype.domein', read_only=True)
    rsin = serializers.CharField(source='zaaktype.rsin', read_only=True)

    class Meta:
        model = StatusType
        fields = (
            'url',
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
        extra_kwargs = {
            'url': {'view_name': 'rest_api:statustypen-detail'}
        }


class ZaakSerializer(serializers.HyperlinkedModelSerializer):
    heeft_als_betrokkene = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='rol_set',
        view_name='rest_api:natuurlijke-personen-detail',
    )

    heeft = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='status_set',
        view_name='rest_api:zaken_statussen-detail',
        parent_lookup_kwargs={
            'zaken_pk': 'zaak__pk'
        }
    )

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
            'informatieobjecten',  # kent
            'rol_set',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:zaken-detail'},
            'zaaktype': {'view_name': 'rest_api:zaaktypen-detail'},
            'rol_set': {'view_name': 'rest_api:rollen-detail'},
            'informatieobjecten': {'view_name': 'rest_api:informatieobjecten-detail'},
        }


class NatuurlijkPersoonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NatuurlijkPersoon
        fields = (
            'url',
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
        extra_kwargs = {
            'url': {'view_name': 'rest_api:natuurlijke-personen-detail'},
        }


class ZaakTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZaakType
        fields = (
            'url',
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
        extra_kwargs = {
            'url': {'view_name': 'rest_api:zaaktypen-detail'},
        }


class StatusSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaken_pk': 'zaak__pk'
    }
    class Meta:
        model = Status
        fields = (
            'url',
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
        extra_kwargs = {
            'url': {'view_name': 'rest_api:zaken_statussen-detail'},
            'status_type': {'view_name': 'rest_api:statustypen-detail'},
            'rol': {'view_name': 'rest_api:rollen-detail'},
        }


class KlantcontactSerializer(serializers.HyperlinkedModelSerializer):
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
            'medewerker',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:klantcontacten-detail'},
            'zaak': {'view_name': 'rest_api:zaken-detail'},
            'natuurlijk_persoon': {'view_name': 'rest_api:natuurlijke-personen-detail'},
            'medewerker': {'view_name': 'rest_api:medewerkers-detail'},
        }


class MedewerkerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medewerker
        fields = (
            'url',
            'medewerkeridentificatie',
            # 'organisatie',
            'achternaam',
            'emailadres',
            'voorletters',
            'voorvoegsel_achternaam',
            'geslachtsaanduiding',
            'datum_uit_dienst',
            'medewerkertoelichting',
            'functie',
            'roepnaam',
            'telefoonnummer',
            # 'StUF:tijdvakGeldigheid',
            # 'StUF:tijdstipRegistratie',
            # 'StUF:extraElementen',
            # 'StUF:aanvullendeElementen',
            # 'historieMaterieel',
            # 'historieFormeel',
            # 'hoortBij',
            # 'isContactpersoonVoor',
            # 'isVerantwoordelijkVoor',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:medewerkers-detail'},
        }


class InformatieObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InformatieObject
        fields = (
            'url',
            'informatieobjectidentificatie',
            'bronorganisatie',
            'creatiedatum',
            'ontvangstdatum',
            'afzender',
            # 'typering',
            'titel',
            'beschrijving',
            'versie',
            'informatieobject_status',
            'verzenddatum',
            'geadresseerde',
            'vertrouwlijkaanduiding',
            'archiefnominatie',
            'archiefactiedatum',
            'auteur',
            'verschijningsvorm',
            # 'eib.formaat',
            # 'eib.taal',
            # 'eib.inhoud',
            # 'eib.link',
            # 'eib.bestandsomvang',
            # 'bestandsnaamEnkelvoudigInformatieobject',
            # 'gebruiksrechtenInformatieobject',
            # 'informatieobjecttype',
            # 'integriteitEnkelvoudigInformatieobject',
            # 'ondertekeningInformatieobject',
            # 'historieMaterieel',
            # 'historieFormeel',
            # 'isBekendBij',
            # 'isOnderdeelVan',
            # 'isOntvangenVanOfVerzondenAan',
            # 'kanVastleggingZijnVan',
            # 'omvat',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:informatieobjecten-detail'},
        }
