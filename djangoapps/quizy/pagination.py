from rest_framework.pagination import PageNumberPagination


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class SmallListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class LessonPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'