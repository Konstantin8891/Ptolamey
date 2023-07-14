from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    RangeFilter,
    DateFromToRangeFilter,
)
from django.db.models import Q
from django.db.models.query import QuerySet

from booking.models import Room, BookingUser


class RoomSearchFilter(FilterSet):
    cost = RangeFilter()
    population = RangeFilter()
    date = DateFromToRangeFilter(method='filter_date')

    def filter_date(
        self, queryset: QuerySet, name: str, value: slice
    ) -> QuerySet:
        bu_qs_bad = BookingUser.objects.filter((
            Q(date_start__lte=value.start) & Q(date_end__gt=value.start)
        ) | (Q(date_start__lt=value.stop) & Q(date_end__gte=value.stop)) | (
            Q(date_start__gte=value.start) & Q(date_end__lte=value.stop)
        )).all().values('room')
        rooms = [el['id'] for el in Room.objects.all().values('id')]
        for el in bu_qs_bad:
            rooms.remove(el['room'])
        return queryset.filter(id__in=rooms)

    class Meta:
        model = Room
        fields = ['cost', 'population', 'date']
