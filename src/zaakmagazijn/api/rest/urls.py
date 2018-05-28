from django.conf.urls import include, url

from rest_framework_nested import routers

from .schema import schema_view
from .views import (
    InformatieObjectViewSet, KlantcontactViewSet, MedewerkerViewSet,
    NatuurlijkPersoonViewSet, RolViewSet, StatusTypeViewSet, StatusViewSet,
    ZaakTypeViewSet, ZaakViewSet
)

root_router = routers.DefaultRouter()
root_router.register(r'rollen', RolViewSet, base_name='rollen')
root_router.register(r'statustypen', StatusTypeViewSet, base_name='statustypen')
root_router.register(r'klantcontacten', KlantcontactViewSet, base_name='klantcontacten')
root_router.register(r'medewerkers', MedewerkerViewSet, base_name='medewerkers')
root_router.register(r'informatieobjecten', InformatieObjectViewSet, base_name='informatieobjecten')
root_router.register(r'zaaktypen', ZaakTypeViewSet, base_name='zaaktypen')  # parents_query_lookups=['zaak']
root_router.register(r'zaken', ZaakViewSet, base_name='zaken')
root_router.register(r'natuurlijke-personen', NatuurlijkPersoonViewSet, base_name='natuurlijke-personen')  # parents_query_lookups=['zaken']

zaken_router = routers.NestedSimpleRouter(root_router, r'zaken', lookup='zaken')
zaken_router.register(r'statussen', StatusViewSet, base_name='zaken_statussen') #  parents_query_lookups=['zaak']


API_PREFIX = r'^v(?P<version>\d+)'


urlpatterns = [
    url(r'{}/schema(?P<format>.json|.yaml)$'.format(API_PREFIX), schema_view.without_ui(cache_timeout=None), name='api-schema-json'),
    url(r'{}/schema/$'.format(API_PREFIX), schema_view.with_ui('redoc', cache_timeout=None), name='api-schema'),

    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(zaken_router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
