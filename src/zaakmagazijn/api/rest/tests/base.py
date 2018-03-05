from django.test import TestCase

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


class AuthenticationTestMixin(object):
    def _authenticate(self):
        org = OrganisationFactory(name='test_org')
        self.client.credentials(HTTP_X_NLX_ORGANISATION_CN=org.name)

    def test_list_view_needs_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})

    def test_detail_view_needs_to_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Authenticatiegegevens zijn niet opgegeven.'})


class APIVersionTestMixin(object):
    API_VERSION = '1'


class APITestCase(APIVersionTestMixin, AuthenticationTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.client = APIClient(content_type='application/json', enforce_csrf_checks=True)
