from django.conf.urls import include, url

from rest_framework_extensions.routers import (
    ExtendedDefaultRouter as DefaultRouter
)

from .views import (
    InformatieObjectViewSet, KlantcontactViewSet, MedewerkerViewSet,
    NatuurlijkPersoonViewSet, RolViewSet, StatusTypeViewSet, StatusViewSet,
    ZaakTypeViewSet, ZaakViewSet
)

from .schema import schema_view

nested_router = DefaultRouter()
zaken_routes = nested_router.register(
    r'zaken',
    ZaakViewSet,
    base_name='zaken',
)
zaken_routes.register(
    r'betrokkenen',
    NatuurlijkPersoonViewSet,
    base_name='zaken_betrokkenen',
    parents_query_lookups=['zaken']
)
zaken_routes.register(
    r'zaaktype',
    ZaakTypeViewSet,
    base_name='zaken_zaaktype',
    parents_query_lookups=['zaak']
)
zaken_routes.register(
    r'status',
    StatusViewSet,
    base_name='zaken_status',
    parents_query_lookups=['zaak']
)
nested_router.register(r'rollen', RolViewSet, base_name='rollen')
nested_router.register(r'statustypen', StatusTypeViewSet, base_name='statustypen')
nested_router.register(r'klantcontact', KlantcontactViewSet, base_name='klantcontact')
nested_router.register(r'medewerker', MedewerkerViewSet, base_name='medewerker')
nested_router.register(r'informatieobject', InformatieObjectViewSet, base_name='informatieobject')


API_PREFIX = r'^v(?P<version>\d+)'


urlpatterns = [
    url(r'{}/schema(?P<format>.json|.yaml)$'.format(API_PREFIX), schema_view.without_ui(cache_timeout=None), name='api-schema-json'),
    url(r'{}/schema/$'.format(API_PREFIX), schema_view.with_ui('redoc', cache_timeout=None), name='api-schema'),

    url(r'^', include(nested_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
