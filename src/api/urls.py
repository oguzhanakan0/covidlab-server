from django.urls import path, include, re_path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'locations', views.LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'locations/blackout-slots/(?P<location>[^/.]+)',
            views.AppointmentBlackoutSlotsAPIView.as_view(), name="blackout_slots"),
    path('users/signin/', views.SigninView.as_view()),
    path('labtest/make-appointment/', views.MakeAppointmentView.as_view())
]
