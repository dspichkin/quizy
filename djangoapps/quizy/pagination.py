from rest_framework.pagination import PageNumberPagination


class CourseListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'