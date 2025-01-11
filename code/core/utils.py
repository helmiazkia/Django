from ninja.pagination import PaginationBase
from ninja import Schema

class CustomPagination(PaginationBase):
    class Input(Schema):
        skip: int

    class Output(Schema):
        items: list
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip:skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }
