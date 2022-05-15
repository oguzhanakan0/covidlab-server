from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.PanelView.as_view()),
    path('search-appointments/', views.PanelSearchView.as_view()),
    path('set-attendance/', views.SetAttendanceView.as_view()),
    path('set-result/', views.SetResultView.as_view()),
]
