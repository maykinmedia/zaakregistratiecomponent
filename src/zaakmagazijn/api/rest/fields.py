from rest_framework.serializers import HyperlinkedRelatedField, HyperlinkedIdentityField


class WithInstanceMixin(object):
    def use_pk_only_optimization(self):
        return True

    def to_representation(self, value, instance=None):
        self.instance = instance
        return super().to_representation(value)

    def get_source(self, obj):
        if self.instance:
            return self.instance
        return obj


class NestedHyperlinkedRelatedField(WithInstanceMixin, HyperlinkedRelatedField):
    def __init__(self, view_name=None, lookup_kwargs={}, **kwargs):
        self.lookup_kwargs = lookup_kwargs
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = {}
        for k, v in self.lookup_kwargs.items():
            args = v.split('.')
            source = self.get_source(obj)
            for arg in args:
                source = getattr(source, arg, arg)
            kwargs[k] = source

        kwargs.update({self.lookup_url_kwarg: getattr(obj, self.lookup_field)})
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class NestedRequestHyperlinkedRelatedField(WithInstanceMixin, HyperlinkedIdentityField):
    def __init__(self, view_name=None, lookup_kwargs={}, **kwargs):
        self.lookup_kwargs = lookup_kwargs
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = {}
        for key, value in self.lookup_kwargs.items():
            if request.kwargs and request.kwargs.get(value):
                kwargs[key] = request.kwargs.get(value)

        kwargs.update({self.lookup_url_kwarg: getattr(self.get_source(obj), self.lookup_field)})
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class ParentHyperlinkedRelatedField(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {}
        if request.kwargs and request.kwargs.get(self.lookup_field):
            kwargs[self.lookup_url_kwarg] = request.kwargs.get(self.lookup_field)

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
