import datetime

from django.db.models import QuerySet
from django.utils import timezone
from django_filters import rest_framework as filters

from api.models import Event


class EventFilter(filters.FilterSet):
    uuid = filters.UUIDFilter(
        field_name="uuid",
    )
    
    within_week = filters.DateFilter(
        field_name="position_groups",
        method="filter_within_week"
    )
    
    def filter_within_week(self, queryset: QuerySet[Event], name, value):
        someday = value
        a_week_later = someday + datetime.timedelta(days=7)
        return queryset.filter(position_groups__positions__date__range=(someday, a_week_later)).distinct()
    
    class Meta:
        model = Event
        fields = [
            "uuid",
            "within_week",
        ]
