from rest_framework.serializers import HyperlinkedIdentityField


class HyperlinkedNestedIdentityField(HyperlinkedIdentityField):

    def __init__(self, view_name=None, lookup_kwargs={}, **kwargs):
        self.lookup_kwargs = lookup_kwargs
        super(HyperlinkedNestedIdentityField, self).__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None
        print()
        kwargs = {}
        for key in self.lookup_kwargs:
            if request.fewefwew and request.fewefwew.get(key):
                kwargs[key] = request.fewefwew.get(key)

        kwargs.update({self.lookup_url_kwarg: getattr(obj, self.lookup_field)})
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)