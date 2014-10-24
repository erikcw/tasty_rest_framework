tasty_rest_framework
====================

A TastyPie compatibility layer for projects migrating to Django Rest Framework.

The project is currently being used in-house to migrate a large TastyPie API to DRF without the API clients having to make any changes.  The new API is in production and has performed without any issues.

Additional docs are in the works.


Installation
------------

Add this libary to your `PYTHONPATH`.

```
pip install -e git://github.com/erikcw/tasty_rest_framework.git#egg=tasty_rest_framework
```


Example
-------

This libaray is composed of a series of mixins that can be added to your `View`/`Viewsets` and `Serializers`


### ViewSets

This ViewSet will use TastyPie style "Token Authentication".  If you'd like to continue to use TastyPie's `ApiKey` model, simply subclass `TastyApiKeyAuthentication` and set it's model attribute like so:

```python
class MyTastyApiKeyAuthentication(TastyApiKeyAuthentication):
    model = ApiKey
```

The `TastyPieViewMixin` alters the pagination style and adds a `/schema/` endpoint.

views.py:

```python

from tasty_rest_framework.authentication import TastyApiKeyAuthentication
from tasty_rest_framework.mixins import TastyPieViewMixin


class UserViewSet(TastyPieViewMixin, viewsets.ReadOnlyModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (TastyPieApiKeyAuthentication,)
    lookup_field = "username"

```

### Serializers

The Serializer mixin adds the `resource_uri` field to your API output.

serializers.py
```python

from tasty_rest_framework.mixins import TastyPieSerializerMixin
from tasty_rest_framework.serializers import TastyPieHyperlinkedIdentityField, TastyPieHyperlinkedRelatedField

class UserSerializer(CCTastyPieSerializerMixin, serializers.HyperlinkedModelSerializer):
    # related field with TastyPie style Hyperlinking defined explicitly
    groups = TastyPieHyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='group-detail',
        lookup_field='pk'
    )


    class Meta:
        model = User
        url_field_name = "resource_uri"
```

That's all there is to it!  The mixins can easily be subclassed to customized behavior further if your TastyPie API has been customized.

## Pull Requests welcome :-)
