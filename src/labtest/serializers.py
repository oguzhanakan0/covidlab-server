from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import LabTest, Location
from django.utils import timezone
from datetime import timedelta


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'address', 'latitude', 'longitude', 'slug']


class BlackoutSlotsSerializer(serializers.Serializer):

    blackout_slots = serializers.SerializerMethodField()

    def get_blackout_slots(self, location):
        now = timezone.now()
        return LabTest.objects.filter(location=location.slug,
                                      test_date__gte=now,
                                      test_date__lte=now+timedelta(days=14))\
            .values_list("test_date", flat=True)