import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from django.http import JsonResponse
from .models import User
from django.forms.models import model_to_dict
import datetime

cred = credentials.Certificate("/Users/oguzhanakan/Desktop/iquit-507f7-firebase-adminsdk-go447-bc8b2413f2.json") # Local Creds
# cred = credentials.Certificate("/home/iquit-507f7-firebase-adminsdk-go447-bc8b2413f2.json") # Server Creds
default_app = firebase_admin.initialize_app(cred)


def sign_in(request):
    print(request.body)  # Debug
    try:
        d = json.loads(request.body)
        id_token = d["token"]
        _user = auth.verify_id_token(id_token)
        print(f"_user: {_user}")  # Debug
        _nuser = {
            "uid":_user["uid"],
            "first_name":" ".join(_user["name"].split(" ")[:-1]),
            "last_name": _user["name"].split(" ")[-1],
            "auth_source": _user["firebase"]["sign_in_provider"],
            "email": _user["email"]
        }
        user, created = User.objects.get_or_create(_nuser)
        print(f"created?: {created}")  # Debug
        if created:
            print("setting first_joined to")
            user.first_joined = datetime.date.today()
            user.save()
        else:
            user.last_login = datetime.date.today()
            user.save()
            print(f"not created: {user.email}, {user.uid}, {user.id}")
        return JsonResponse({
            "success": True,
            "user": model_to_dict(user,fields=["first_name","last_name","is_info_complete","email","username"])
        })
    except:
        return JsonResponse({
            "success": False
        })


def update_user(request):
    print(request.body)  # Debug
    try:
        d = json.loads(request.body)
        print(d)  # Debug
        query = User.objects.filter(uid=d["uid"])
        query.update(**d | {"is_info_complete": True})
        return JsonResponse({
            "success": True,
            "user": model_to_dict(query[0],fields=["first_name","last_name","is_info_complete","email","username"])
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })