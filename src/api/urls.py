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
    path('users/change-name/', views.ChangeNameView.as_view()),
    path('users/appointments/', views.GetAppointmentsView.as_view()),
    path('labtest/make-appointment/', views.MakeAppointmentView.as_view()),
    path('labtest/update-appointment/', views.UpdateAppointmentView.as_view()),
    path('labtest/cancel-appointment/', views.CancelAppointmentView.as_view()),
    path('labtest/make-payment/', views.MakePaymentView.as_view()),
    re_path(r'labtest/verify/(?P<id>[^/.]+)',
            views.VerifyTestResultView.as_view(), name="result_verify"),
]
