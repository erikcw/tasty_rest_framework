from rest_framework import pagination, serializers
from rest_framework.templatetags.rest_framework import replace_query_param


class CursorToPageMixin(object):

    def page_to_offset(self, page_number, page_size):
        if page_number is 1:
            offset = 0
        else:
            offset = (page_number - 1) * page_size
        return offset


class OffsetField(CursorToPageMixin, serializers.Field):
    """
    Field that returns the offset of the current page.
    """

    def to_native(self, value):
        return self.page_to_offset(value.number, value.paginator.per_page)


class NextPageField(CursorToPageMixin, serializers.Field):
    """
    Field that returns a link to the next page in paginated results.
    """
    page_field = 'offset'
    limit_field = 'limit'

    def to_native(self, value):
        if not value.has_next():
            return None
        page = value.next_page_number()
        limit = value.paginator.per_page
        page = self.page_to_offset(page, limit)
        request = self.context.get('request')
        url = request and request.build_absolute_uri() or ''
        url = replace_query_param(url, self.page_field, page)
        url = replace_query_param(url, self.limit_field, limit)
        return url


class PreviousPageField(CursorToPageMixin, serializers.Field):
    """
    Field that returns a link to the previous page in paginated results.
    """
    page_field = 'offset'
    limit_field = 'limit'

    def to_native(self, value):
        if not value.has_previous():
            return None
        page = value.previous_page_number()
        limit = value.paginator.per_page
        page = self.page_to_offset(page, limit)
        request = self.context.get('request')
        url = request and request.build_absolute_uri() or ''
        url = replace_query_param(url, self.page_field, page)
        url = replace_query_param(url, self.limit_field, limit)
        return url


class MetaSerializer(serializers.Serializer):
    next = NextPageField(source='*')
    previous = PreviousPageField(source='*')
    total_count = serializers.Field(source='paginator.count')
    limit = serializers.Field(source='paginator.per_page')
    offset = OffsetField(source='*')


class TastyPaginationSerializer(pagination.BasePaginationSerializer):
    meta = MetaSerializer(source='*')
    
    results_field = 'objects'
