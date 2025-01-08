import django_filters
from reviews.models import Review

class ReviewFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte', required=False)
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte', required=False)

    class Meta:
        model = Review
        fields = ['min_rating', 'max_rating']