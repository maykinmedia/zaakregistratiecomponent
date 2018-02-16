from rest_framework.serializers import HyperlinkedIdentityField


class NestedHyperlinkedIdentityField(HyperlinkedIdentityField):
    def __init__(self, view_name=None, lookup_kwargs={}, **kwargs):
        self.lookup_kwargs = lookup_kwargs
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None

        kwargs = {}
        print(obj)
        print(type(obj))
        for k, v in self.lookup_kwargs.items():
            args = v.split('.')
            source = obj
            for arg in args:
                source = getattr(source, arg, arg)
            kwargs[k] = source

        kwargs.update({self.lookup_url_kwarg: getattr(obj, self.lookup_field)})
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class NestedRequestHyperlinkedIdentityField(HyperlinkedIdentityField):
    def __init__(self, view_name=None, lookup_kwargs={}, **kwargs):
        self.lookup_kwargs = lookup_kwargs
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None

        kwargs = {}
        for key, value in self.lookup_kwargs.items():
            if request.kwargs and request.kwargs.get(value):
                kwargs[key] = request.kwargs.get(value)

        kwargs.update({self.lookup_url_kwarg: getattr(obj, self.lookup_field)})
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class ParentHyperlinkedIdentityField(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None

        kwargs = {}
        if request.kwargs and request.kwargs.get(self.lookup_field):
            kwargs[self.lookup_url_kwarg] = request.kwargs.get(self.lookup_field)

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
