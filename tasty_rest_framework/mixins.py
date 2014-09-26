from .pagination import TastyPaginationSerializer
from .renderers import TastyPieJSONRenderer
from .exceptions import MixinException
from .serializers import TastyPieHyperlinkedIdentityField, TastyPieHyperlinkedRelatedField
import rest_framework.renderers


class TastyPieViewMixin(object):
    """
    Use this mixin with Views and Viewsets to achieve TastyPie like
    funcionality.
    """
    pagination_serializer_class = TastyPaginationSerializer
    renderer_classes = (TastyPieJSONRenderer, rest_framework.renderers.BrowsableAPIRenderer)

    paginate_by_param = 'limit'
    paginate_offset_param = 'offset'

    def paginate_queryset(self, queryset, page_size=None):
        """
        Tastypie style pagination.
        """
        page = super(TastyPieViewMixin, self).paginate_queryset(queryset, page_size=page_size)

        if page is None:
            return page

        offset = self.request.GET.get(self.paginate_offset_param)
        if offset:
            # convert cursor into page number and fetch page
            limit = page.paginator.per_page
            page_number = (int(offset) / limit) + 1
            page = page.paginator.page(page_number)

        return page


class TastyPieSerializerMixin(object):
    """
    Modify serializer to behave like TastyPie
    """

    _hyperlink_field_class = TastyPieHyperlinkedRelatedField
    _hyperlink_identify_field_class = TastyPieHyperlinkedIdentityField

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
