from django_filters import rest_framework as filters


class RestaurantFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')
    description = filters.CharFilter(field_name='description')