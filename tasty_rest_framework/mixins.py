from django.core.paginator import EmptyPage
from django.http import Http404
from .pagination import TastyPagination
from .renderers import TastyPieJSONRenderer
from .exceptions import MixinException
from .serializers import TastyPieHyperlinkedIdentityField, TastyPieHyperlinkedRelatedField
from rest_framework.decorators import list_route
import rest_framework.renderers



class TastyPieViewMixin(object):
    """
    Use this mixin with Views and Viewsets to achieve TastyPie like
    funcionality.
    """
    renderer_classes = (TastyPieJSONRenderer, rest_framework.renderers.BrowsableAPIRenderer)
    pagination_class = TastyPagination

    @list_route(methods=['get', 'post'])
    def schema(self, request, *args, **kwargs):
        """
        For backwords compatability with Tastypie add a schema endpoint.

        This simply forwards off an OPTIONS request, which is the preferred
        method of accessing this view.
        """
        # need to accept POST so that actions will be displayed in the output.
        return self.options(request, *args, **kwargs)



class TastyPieSerializerMixin(object):
    """
    Modify serializer to behave like TastyPie
    """

    serializer_related_field = TastyPieHyperlinkedRelatedField
    serializer_url_field = TastyPieHyperlinkedIdentityField

    def __init__(self, *args, **kwargs):
        self._patch_meta()
        super(TastyPieSerializerMixin, self).__init__(*args, **kwargs)

    def _patch_meta(self):
        """
        Update the Serializer's inner Meta class settings with those needed
        for TastyPie compatibility.
        """
        error_msg = "{0} already has {1} set on its Meta class. Remove it to continue."
        attr_name = 'url_field_name'
        attr_value = 'resource_uri'
        if hasattr(self.Meta, attr_name) and getattr(self.Meta, attr_name, None) != attr_value:
            raise MixinException(error_msg.format(repr(self), attr_name))
        setattr(self.Meta, attr_name, attr_value)


