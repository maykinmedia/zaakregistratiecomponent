from django.conf.urls import include, url

from rest_framework_extensions.routers import (
    ExtendedDefaultRouter as DefaultRouter
)

from .views import NatuurlijkPersoonViewSet, RolViewSet, ZaakViewSet

nested_router = DefaultRouter()
nested_router.register(
    r'zaken',
    ZaakViewSet,
    base_name='zaken',
).register(
    r'betrokkenen',
    NatuurlijkPersoonViewSet,
    base_name='zaken_betrokkenen',
    parents_query_lookups=['zaken']
)
nested_router.register(r'rollen', RolViewSet, base_name='rollen')

# router = DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^', include(nested_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns += nested_router.urls
