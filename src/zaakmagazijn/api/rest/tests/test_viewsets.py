import json

from django.urls import reverse

from ....rgbz.tests.factory_models import (
    InformatieObjectFactory, KlantcontactFactory, MedewerkerFactory,
    NatuurlijkPersoonFactory, RolFactory, StatusFactory, StatusTypeFactory,
    ZaakFactory, ZaakTypeFactory
)
from .base import APITestCase, ReadOnlyViewSetMixin
from ....rgbz.models import Klantcontact


class TestZaakViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.zaak = ZaakFactory()

        self.list_url = reverse('rest_api:zaken-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:zaken-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.zaak.id
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestRolViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.rol = RolFactory()

        self.list_url = reverse('rest_api:rollen-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:rollen-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.rol.id
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestStatusTypeViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.status_type = StatusTypeFactory()

        self.list_url = reverse('rest_api:statustypen-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:statustypen-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.status_type.id
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestKlantcontactViewSet(APITestCase):
    def setUp(self):
        super().setUp()

        self.zaak = ZaakFactory()
        self.natuurlijk_persoon = NatuurlijkPersoonFactory()
        self.medewerker = MedewerkerFactory()
        self.klantcontact = KlantcontactFactory(zaak=self.zaak, medewerker=self.medewerker)

        self.list_url = reverse('rest_api:klantcontacten-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:klantcontacten-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.klantcontact.id
        })

    def _get_required_urls(self):
        zaak_url = reverse('rest_api:zaken-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.zaak.id
        })
        natuurlijk_persoon_url = reverse('rest_api:natuurlijke-personen-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.natuurlijk_persoon.id,
        })
        medewerker_url = reverse('rest_api:medewerkers-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.medewerker.id
        })
        return zaak_url, natuurlijk_persoon_url, medewerker_url

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
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

        response = self.client.post(self.list_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontacten-detail', kwargs={
            'version': self.API_VERSION,
            'pk': klantcontact.id
        })
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

        response = self.client.post(self.list_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontacten-detail', kwargs={
            'version': self.API_VERSION,
            'pk': klantcontact.id
        })
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

        response = self.client.put(self.detail_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200, msg=response.data)

        klantcontact = Klantcontact.objects.last()
        url = reverse('rest_api:klantcontacten-detail', kwargs={
            'version': self.API_VERSION,
            'pk': klantcontact.id
        })
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


class TestNatuurlijkPersoonViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.natuurlijk_persoon = NatuurlijkPersoonFactory()

        self.list_url = reverse('rest_api:natuurlijke-personen-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:natuurlijke-personen-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.natuurlijk_persoon.id,
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestZaakTypeViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.zaak_type = ZaakTypeFactory()

        self.list_url = reverse('rest_api:zaaktypen-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:zaaktypen-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.zaak_type.id,
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestStatusViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.zaak = ZaakFactory()
        self.natuurlijk_persoon = NatuurlijkPersoonFactory()
        self.rol = RolFactory(zaak=self.zaak, betrokkene=self.natuurlijk_persoon)
        self.status_type = StatusTypeFactory()
        self.medewerker = MedewerkerFactory()
        self.status = StatusFactory(zaak=self.zaak, rol=self.rol, status_type=self.status_type)

        self.list_url = reverse('rest_api:zaken_statussen-list', kwargs={
            'version': self.API_VERSION,
            'zaken_pk': self.zaak.pk,
        })
        self.detail_url = reverse('rest_api:zaken_statussen-detail', kwargs={
            'version': self.API_VERSION,
            'zaken_pk': self.zaak.pk,
            'pk': self.status.id,
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestMedewerkerViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.medewerker = MedewerkerFactory()

        self.list_url = reverse('rest_api:medewerkers-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:medewerkers-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.medewerker.id
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))


class TestInformatieObjectViewSet(ReadOnlyViewSetMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.informatie_object = InformatieObjectFactory()

        self.list_url = reverse('rest_api:informatieobjecten-list', kwargs={
            'version': self.API_VERSION,
        })
        self.detail_url = reverse('rest_api:informatieobjecten-detail', kwargs={
            'version': self.API_VERSION,
            'pk': self.informatie_object.id
        })

    def test_list_view(self):
        self._authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'http://testserver{}'.format(self.detail_url))

    def test_detail_view(self):
        self._authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], 'http://testserver{}'.format(self.detail_url))
