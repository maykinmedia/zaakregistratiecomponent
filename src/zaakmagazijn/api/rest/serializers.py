from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField

from zaakmagazijn.rgbz.models.betrokkene import NatuurlijkPersoon, Rol
from zaakmagazijn.rgbz.models.zaken import Zaak

from .fields import HyperlinkedNestedIdentityField


class RolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rol
        fields = (
            'rolomschrijving',
            'rolomschrijving_generiek',
            'roltoelichting',
            'indicatie_machtiging',
        )


class ZaakSerializer(serializers.HyperlinkedModelSerializer):
    rol_set = serializers.HyperlinkedRelatedField(
        view_name='rest_api:rollen-detail',
        many=True,
        read_only=True
    )
    # betrokkene_set = serializers.HyperlinkedRelatedField(
    #     view_name='rest_api:zaken_betrokkenen-detail',
    #     lookup_field='pk',
    #     many=True,
    #     read_only=True
    # )

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
            # 'zaaktype',
            # 'historieMaterieel',
            # 'historieFormeel',
            # 'betreft',
            'heeft',
            # 'heeft_als_adviseur',
            # 'heeft_als_behandelaar',
            # 'heeft_als_belanghebbende',
            # 'heeft_als_beslisser',
            # 'heeft_als_betrokkene',
            # # 'heeft_als_deelzaken',
            # 'heeft_als_initiator',
            # 'heeft_als_klantcontacter',
            # # 'heeft_als_mede_initiator',
            # # 'heeft_als_uitkomst',
            # 'heeft_als_zaakcoordinator',
            # # 'heeft_contact',
            # # 'heeft_relevante_andere',
            'is_deelzaak_van',
            # # 'is_relevant_voor',
            'kent',
            'rol_set',
            # 'betrokkene_set',
        )
        extra_kwargs = {
            'url': {'view_name': 'rest_api:zaken-detail', 'lookup_field': 'pk'},
        }


class NatuurlijkPersoonSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedNestedIdentityField(
        view_name='rest_api:zaken_betrokkenen-detail',
        lookup_kwargs=[
            "parent_lookup_zaken"
        ],
        read_only=True,
        # many=True
    )

    class Meta:
        model = NatuurlijkPersoon
        fields = (
            'url',
            'burgerservicenummer',
        )

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs.get('context').get('kwargs')
        super().__init__(*args, **kwargs)

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        kwargs.update(url=self.kwargs)
        return kwargs
