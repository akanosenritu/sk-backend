from django_filters import rest_framework as filters

from api.models import Event


class EventFilter(filters.FilterSet):
    uuid = filters.UUIDFilter(name="uuid")
    
    class Meta:
        model = Event
        fields = ["uuid"]
