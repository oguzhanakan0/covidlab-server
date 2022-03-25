import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone
from django.forms.models import model_to_dict

from labtest.serializers import LocationSerializer, BlackoutSlotsSerializer
from labtest.models import LabTest, Location
from user.models import User


cred = credentials.Certificate("src/firebase-credentials.json")  # Local Creds
default_app = firebase_admin.initialize_app(cred)


class MakeAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            # print("make appointment request received.") # Debug
            # print(request.user) # Debug
            # print(request.user.email) # Debug
            # print(request.body) # Debug
            d = json.loads(request.body)
            labtest = LabTest(user=request.user,
                              test_date=d["test_date"],
                              location=Location.objects.get(slug=d["location"]))
            if len(LabTest.objects.filter(
                    location=labtest.location,
                    test_date=labtest.test_date)) != 0:
                raise Exception(
                    "The slot you picked is no longer available. Please select a different timeslot and submit again.")
            labtest.save()
            # LabTest(d)
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "detail": str(e)
            }, status=500)


class SigninView(ObtainAuthToken):

    def post(self, request):
        print("signin request received.")
        # print(request.body)  # Debug

        d = json.loads(request.body)
        id_token = d["token"]
        _user = auth.verify_id_token(id_token)
        # print(f"_user: {_user}")  # Debug

        user, created = User.objects.get_or_create(
            uid=_user["uid"],
            auth_source=_user["firebase"]["sign_in_provider"],
            email=_user["email"]
        )
        # print(f"user: {user}")  # Debug

        if created:
            user.first_joined = timezone.now()
            user.save()
        else:
            user.last_login = timezone.now()
            user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "success": True,
            'token': token.key,
            'user': model_to_dict(user, fields=["first_name", "last_name", "is_info_complete", "email", "username"]),
        })


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class AppointmentBlackoutSlotsAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = BlackoutSlotsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.filter(slug=self.kwargs.get("location"))
        return queryset
