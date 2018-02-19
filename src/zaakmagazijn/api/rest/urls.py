from django.conf.urls import include, url

from rest_framework_extensions.routers import (
    ExtendedDefaultRouter as DefaultRouter
)

from .views import (
    KlantcontactViewSet, NatuurlijkPersoonViewSet, RolViewSet,
    StatusTypeViewSet, StatusViewSet, ZaakTypeViewSet, ZaakViewSet
)

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

urlpatterns = [
    url(r'^', include(nested_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
