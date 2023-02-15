from django_filters import rest_framework as filters

from reviews.models import Title


class FilterForTitle(filters.FilterSet):
    """Описание фильтрации по полям модели Title для ViewSet."""
    name = filters.CharFilter(field_name='name')
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
