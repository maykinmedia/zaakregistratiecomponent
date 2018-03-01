from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from ....apiauth.tests.factory_models import OrganisationFactory
from ....rgbz.models import (
    InformatieObject, Klantcontact, Medewerker, NatuurlijkPersoon, Rol, Status,
    StatusType, Zaak, ZaakType
)
from ....rgbz.tests.factory_models import (
    InformatieObjectFactory, KlantcontactFactory, MedewerkerFactory,
    NatuurlijkPersoonFactory, RolFactory, StatusFactory, StatusTypeFactory,
    ZaakFactory, ZaakTypeFactory
)


class CreateDataMixin(object):
    def setUp(self):
        super().setUp()

        self.zaak_type = ZaakTypeFactory()
        self.zaak = ZaakFactory(zaaktype=self.zaak_type)
        self.natuurlijk_persoon = NatuurlijkPersoonFactory()
        self.rol = RolFactory(zaak=self.zaak, betrokkene=self.natuurlijk_persoon)
        self.status_type = StatusTypeFactory()
        self.medewerker = MedewerkerFactory()
        self.klantcontact = KlantcontactFactory(zaak=self.zaak, medewerker=self.medewerker)
        self.status = StatusFactory(zaak=self.zaak, rol=self.rol, status_type=self.status_type)
        self.informatie_object = InformatieObjectFactory()
        self.assertEqual(Zaak.objects.count(), 1)
        self.assertEqual(NatuurlijkPersoon.objects.count(), 1)
        self.assertEqual(Rol.objects.count(), 1)
        self.assertEqual(StatusType.objects.count(), 1)
        self.assertEqual(Klantcontact.objects.count(), 1)
        self.assertEqual(ZaakType.objects.count(), 2)
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(Medewerker.objects.count(), 1)
        self.assertEqual(InformatieObject.objects.count(), 1)

        self.client = APIClient(enforce_csrf_checks=True)

    def _authenticate(self):
        org = OrganisationFactory(name='test_org')
        self.client.credentials(HTTP_X_NLX_ORGANISATION_CN=org.name)


class ReadOnlyViewSetMixin(object):
    def test_post_list(self):
        self._authenticate()
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, 405)

    def test_delete_list(self):
        self._authenticate()
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, 405)

    def test_put_list(self):
        self._authenticate()
        response = self.client.put(self.list_url)
        self.assertEqual(response.status_code, 405)

    def test_post_detail(self):
        self._authenticate()
        response = self.client.post(self.detail_url)
        self.assertEqual(response.status_code, 405)

    def test_delete_detail(self):
        self._authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 405)

    def test_put_detail(self):
        self._authenticate()
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, 405)


class TestZaakViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:zaken-list')
        self.detail_url = reverse('rest_api:zaken-detail', kwargs={'pk': self.zaak.id})

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 25)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestRolViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:rollen-list')
        self.detail_url = reverse('rest_api:rollen-detail', kwargs={'pk': self.rol.id})

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestStatusTypeViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:statustypen-list')
        self.detail_url = reverse('rest_api:statustypen-detail', kwargs={'pk': self.status_type.id})

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestKlantcontactViewSet(CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:klantcontact-list')
        self.detail_url = reverse('rest_api:klantcontact-detail', kwargs={'pk': self.klantcontact.id})

    def _get_required_urls(self):
        zaak_url = reverse('rest_api:zaken-detail', kwargs={'pk': self.zaak.id})
        natuurlijk_persoon_url = reverse('rest_api:zaken_betrokkenen-detail', kwargs={
            'pk': self.natuurlijk_persoon.id,
            'parent_lookup_zaken': self.zaak.id
        })
        medewerker_url = reverse('rest_api:medewerker-detail', kwargs={'pk': self.medewerker.id})
        return zaak_url, natuurlijk_persoon_url, medewerker_url

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))

    def test_post_empty_object(self):
        self._authenticate()
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, 400, msg=response.data)
        self.assertEqual(response.data, {
            'identificatie': ['Dit veld is vereist.'],
            'datumtijd': ['Dit veld is vereist.'],
            'onderwerp': ['Dit veld is vereist.'],
            'zaak': ['Dit veld is vereist.'],
            'natuurlijk_persoon': ['Dit veld is vereist.'],
            'medewerker': ['Dit veld is vereist.']
        })

    def test_post_required_fields(self):
        self._authenticate()

        zaak_url, natuurlijk_persoon_url, medewerker_url = self._get_required_urls()

        data = {
            'identificatie': '1234554321',
            'datumtijd': '2018',
            'onderwerp': 'Dit is het onderwerp',
            'zaak': zaak_url,
            'natuurlijk_persoon': natuurlijk_persoon_url,
            'medewerker': medewerker_url,
        }

        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, 201, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontact-detail', kwargs={'pk': klantcontact.id})
        self.assertEqual(response.data, {
            'url': 'http://testserver{}'.format(url),
            'identificatie': '1234554321',
            'datumtijd': '2018',
            'kanaal': None,
            'onderwerp': 'Dit is het onderwerp',
            'toelichting': None,
            'zaak': 'http://testserver{}'.format(zaak_url),
            'natuurlijk_persoon': 'http://testserver{}'.format(natuurlijk_persoon_url),
            'medewerker': 'http://testserver{}'.format(medewerker_url)
        })

    def test_post_all_fields(self):
        self._authenticate()

        zaak_url, natuurlijk_persoon_url, medewerker_url = self._get_required_urls()

        data = {
            'identificatie': '1234554321',
            'datumtijd': '2018',
            'onderwerp': 'Dit is het onderwerp',
            'zaak': zaak_url,
            'natuurlijk_persoon': natuurlijk_persoon_url,
            'medewerker': medewerker_url,
            'kanaal': '2',
            'toelichting': 'Dit is een toelichting',
        }

        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, 201, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontact-detail', kwargs={'pk': klantcontact.id})
        self.assertEqual(response.data, {
            'url': 'http://testserver{}'.format(url),
            'identificatie': '1234554321',
            'datumtijd': '2018',
            'kanaal': '2',
            'onderwerp': 'Dit is het onderwerp',
            'toelichting': 'Dit is een toelichting',
            'zaak': 'http://testserver{}'.format(zaak_url),
            'natuurlijk_persoon': 'http://testserver{}'.format(natuurlijk_persoon_url),
            'medewerker': 'http://testserver{}'.format(medewerker_url)
        })

    def test_delete_klantcontact(self):
        self._authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204, msg=response.data)

    def test_delete_klantcontact_twice(self):
        self._authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204, msg=response.data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 404, msg=response.data)
        self.assertEqual(response.data, {'detail': 'Niet gevonden.'})

    def test_put_empty_object(self):
        self._authenticate()
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, 400, msg=response.data)
        self.assertEqual(response.data, {
            'identificatie': ['Dit veld is vereist.'],
            'datumtijd': ['Dit veld is vereist.'],
            'onderwerp': ['Dit veld is vereist.'],
            'zaak': ['Dit veld is vereist.'],
            'natuurlijk_persoon': ['Dit veld is vereist.'],
            'medewerker': ['Dit veld is vereist.']
        })

    def test_put_required_fields(self):
        self._authenticate()

        zaak_url, natuurlijk_persoon_url, medewerker_url = self._get_required_urls()

        data = {
            'identificatie': self.klantcontact.identificatie,
            'datumtijd': self.klantcontact.datumtijd,
            'onderwerp': 'Dit is iets anders',
            'zaak': zaak_url,
            'natuurlijk_persoon': natuurlijk_persoon_url,
            'medewerker': medewerker_url,
        }

        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, 200, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontact-detail', kwargs={'pk': klantcontact.id})
        self.assertEqual(response.data, {
            'url': 'http://testserver{}'.format(url),
            'identificatie': self.klantcontact.identificatie,
            'datumtijd': self.klantcontact.datumtijd,
            'kanaal': self.klantcontact.kanaal,
            'onderwerp': 'Dit is iets anders',
            'toelichting': self.klantcontact.toelichting,
            'zaak': 'http://testserver{}'.format(zaak_url),
            'natuurlijk_persoon': 'http://testserver{}'.format(natuurlijk_persoon_url),
            'medewerker': 'http://testserver{}'.format(medewerker_url)
        })


class TestNatuurlijkPersoonViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:zaken_betrokkenen-list', kwargs={
            'parent_lookup_zaken': self.zaak.id
        })
        self.detail_url = reverse('rest_api:zaken_betrokkenen-detail', kwargs={
            'pk': self.natuurlijk_persoon.id,
            'parent_lookup_zaken': self.zaak.id
        })

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestZaakTypeViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:zaken_zaaktype-list', kwargs={
            'parent_lookup_zaak': self.zaak.id
        })
        self.detail_url = reverse('rest_api:zaken_zaaktype-detail', kwargs={
            'pk': self.zaak_type.id,
            'parent_lookup_zaak': self.zaak.id
        })

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 11)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestStatusViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:zaken_status-list', kwargs={
            'parent_lookup_zaak': self.zaak.id
        })
        self.detail_url = reverse('rest_api:zaken_status-detail', kwargs={
            'pk': self.status.id,
            'parent_lookup_zaak': self.zaak.id
        })

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestMedewerkerViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:medewerker-list')
        self.detail_url = reverse('rest_api:medewerker-detail', kwargs={'pk': self.medewerker.id})

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 12)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestInformatieObjectViewSet(ReadOnlyViewSetMixin, CreateDataMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.list_url = reverse('rest_api:informatieobject-list')
        self.detail_url = reverse('rest_api:informatieobject-detail', kwargs={'pk': self.informatie_object.id})

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 17)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))
