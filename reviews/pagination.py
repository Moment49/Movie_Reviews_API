from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    """This is a custom pagination to be used by the movieReviewByTitle class"""
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'
