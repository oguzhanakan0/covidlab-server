from django.urls import path
from django.urls import include, re_path
# from .views import requery_loan_detail


from . import views

urlpatterns=[
    path('sign-in',views.sign_in),
    path('update',views.update_user),
]