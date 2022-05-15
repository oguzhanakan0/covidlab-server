from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from notif.models import Notif
from .authentication import TokenAuthSupportCookie
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.renderers import TemplateHTMLRenderer
from labtest.models import Location, LabTest
import json
import datetime as dt
import pytz
from dateutil.tz import gettz


def login(request):
    # print("login page - user:")
    # print(request.COOKIES)
    # if request.COOKIES.get("auth_token") is not None:
    #     return redirect("/")

    return render(request, 'ui/login.html', {})


def logout(request):
    response = HttpResponse("", {"success": True})
    response.delete_cookie('auth_token')
    return response


class PanelView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = [TokenAuthSupportCookie]

    @staticmethod
    def home_exception_handler(exc, context):
        return redirect("/login")

    def get_exception_handler(self):
        return self.home_exception_handler

    def get(self, request):
        return render(
            request,
            'ui/panel.html',
            {
                "user": request.user,
                "locations": Location.objects.all()
            })


class PanelSearchView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = [TokenAuthSupportCookie]

    def get(self, request):
        # print(request.GET)
        r = request.GET.copy()
        s = dt.datetime.strptime(
            r.get("start-date"), '%m/%d/%Y').astimezone(pytz.utc)
        e = dt.datetime.strptime(
            r.get("end-date"), '%m/%d/%Y').astimezone(pytz.utc)
        l = r.get("location")

        labtests = LabTest.objects.filter(
            test_date__gte=s, test_date__lte=e, location=Location.objects.get(slug=l))
        return render(
            request,
            'ui/widgets/search_results.html',
            {
                "labtests": labtests
            })


class SetAttendanceView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = [TokenAuthSupportCookie]

    def post(self, request):
        print("attendance request received.")
        print(request.body)  # Debug

        d = json.loads(request.body)
        print(d)
        labtest = LabTest.objects.get(id=d["test_id"])
        labtest.attended = d["attended"]
        labtest.save()
        if not labtest.attended:
            Notif(
                user=labtest.user,
                title="Missed Appointment",
                content=f"You missed your appointment on {labtest.test_date.astimezone(gettz('America/Los_Angeles')).strftime('%D at %H:%M')} at {labtest.location.name}. Next time, please try to cancel your appointment if you cannot show up.",
                notif_type="D"
            ).save()
        return render(
            request,
            'ui/widgets/attendance_cell.html',
            {
                "attended": d["attended"]
            })


class SetResultView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = [TokenAuthSupportCookie]

    def post(self, request):
        print("result request received.")
        print(request.body)  # Debug

        d = json.loads(request.body)
        print(d)
        labtest = LabTest.objects.get(id=d["test_id"])
        labtest.result = d["result"]
        labtest.save()
        Notif(
            user=labtest.user,
            title="Test Result Available",
            content=f"Your test result for {labtest.test_date.astimezone(gettz('America/Los_Angeles')).strftime('%D at %H:%M')} at {labtest.location.name} is available. Please check it from the home page.",
            notif_type="W"
        ).save()
        return render(
            request,
            'ui/widgets/result_cell.html',
            {
                "result": d["result"]
            })
