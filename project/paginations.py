import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response


class PageSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request) or self.page_size
        total_pages = math.ceil(self.page.paginator.count / page_size) if page_size else 1

        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page_count": total_pages,
                "results": data,
            }
        )
