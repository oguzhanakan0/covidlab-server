import json
from django.http import HttpResponse
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

from labtest.serializers import LabTestShortSerializer, LocationSerializer, BlackoutSlotsSerializer
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


class VerifyTestResultView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [TokenAuthentication]
    queryset = LabTest.objects.all()
    # serializer_class = BlackoutSlotsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        print(self.kwargs.get("id"))
        queryset = self.queryset.filter(verify_id=self.kwargs.get("id"))
        return queryset

    def get(self, request, id):
        try:
            print("verify test result request received.")  # Debug
            labtest = self.get_queryset()
            if len(labtest) == 0:
                raise Exception("The test does not exist.")
            if len(labtest) > 1:
                raise Exception("This cannot happen.")

            l = labtest[0]
            response_text = f"""<h1>
            {str(l.user.first_name)} {str(l.user.last_name)}
            (DOB: {str(l.user.birth_date)}) has been tested
            {"POSITIVE" if l.result else "NEGATIVE"} for COVID-19 on {str(l.test_date)}.
            </h1>
            """
            # LabTest(d)
            return HttpResponse(response_text)
        except Exception as e:
            return Response({
                "detail": str(e)
            }, status=500)


class UpdateAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            d = json.loads(request.body)
            print("update appointment request received.")
            print(d)
            labtest = LabTest.objects.filter(pk=d["test_id"])
            del d["test_id"]
            labtest.update(**d)
            print(
                f"labtest updated to:\n\
                test_date: {labtest[0].test_date},\
                \npayment_date: {labtest[0].payment_date},\
                \nlocation:{labtest[0].location}"
            )
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "detail": str(e)
            }, status=500)


class CancelAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            d = json.loads(request.body)
            print("cancel appointment request received.")
            print(d)
            labtest = LabTest.objects.filter(pk=d["test_id"])[0]
            labtest.canceled = True
            labtest.save()
            print(
                f"labtest canceled."
            )
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "detail": str(e)
            }, status=500)


class ChangeNameView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            d = json.loads(request.body)
            print("change name request received.")
            print(d)
            user = request.user
            user.first_name = d["first_name"]
            user.last_name = d["last_name"]
            user.save()
            print(f"user's name changed to: {user.first_name, user.last_name}")
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "detail": str(e)
            }, status=500)


class MakePaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            d = json.loads(request.body)
            labtest = LabTest.objects.get(pk=d["test_id"])
            labtest.payment_date = timezone.now()
            labtest.save()
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "detail": "Payment was not successful. Please try again later."
            }, status=500)


class GetAppointmentsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get']
    serializer_class = LabTestShortSerializer
    queryset = LabTest.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user, canceled=False)
        return queryset


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
            'user': model_to_dict(user, fields=["first_name", "last_name", "is_info_complete", "email", "username", "birth_date"]),
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
