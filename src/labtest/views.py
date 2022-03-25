from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from labtest.serializers import LocationSerializer
from labtest.models import LabTest, Location
from django.core import serializers
from rest_framework import viewsets


def locations(request):
    # print("get_locations request received.") # Debug
    # print(request.body)  # Debug
    try:
        return JsonResponse({
            "success": True,
            "locations": serializers.serialize('json',
                                               Location.objects.all(),
                                               fields=('name', 'address', 'latitude', 'longitude', 'slug'))
        })
    except:
        return JsonResponse({
            "success": False
        })


def blackout_dates(request):
    # print(request.body)  # Debug
    try:
        location = request.GET.get("location")
        now = timezone.now()
        return JsonResponse({
            "success": True,
            "blackout_dates": [e.test_date for e in
                               LabTest.objects.filter(
                                   location=location,
                                   test_date__gte=now,
                                   test_date__lte=now+timedelta(days=14))],
        })
    except:
        return JsonResponse({
            "success": False
        })
