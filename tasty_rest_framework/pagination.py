from rest_framework.response import Response
from rest_framework import pagination, serializers
from rest_framework.templatetags.rest_framework import replace_query_param


class TastyPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_count': self.count,
                'limit': self.limit,
                'offset': self.offset,
            },
            'objects': data,
        })
