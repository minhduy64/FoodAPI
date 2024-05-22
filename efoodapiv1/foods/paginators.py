from rest_framework import pagination


class StorePaginator(pagination.PageNumberPagination):
    page_size = 2


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
