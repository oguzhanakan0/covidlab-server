import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from django.http import JsonResponse
from .models import User
from django.forms.models import model_to_dict
import datetime
from django.utils import timezone

# cred = credentials.Certificate("/Users/oguzhanakan/Desktop/iquit-507f7-firebase-adminsdk-go447-bc8b2413f2.json")  # Local Creds
# cred = credentials.Certificate("src/firebase-credentials.json")  # Local Creds
# default_app = firebase_admin.initialize_app(cred)


def sign_in(request):
    pass
    # print("signin request received.")
    # # print(request.body)  # Debug
    # # try:
    # d = json.loads(request.body)
    # id_token = d["token"]
    # _user = auth.verify_id_token(id_token)
    # # print(f"_user: {_user}")  # Debug
    # user, created = User.objects.get_or_create(
    #     uid=_user["uid"],
    #     auth_source=_user["firebase"]["sign_in_provider"],
    #     email=_user["email"]
    # )
    # # print(f"created?: {created}")  # Debug
    # if created:
    #     # print(f"setting first_joined to {datetime.date.today()}")  # Debug
    #     user.first_joined = timezone.now()
    #     user.save()
    # else:
    #     user.last_login = timezone.now()
    #     user.save()
    #     # print(f"not created: {user.email}, {user.uid}, {user.id}")
    # token, created = Token.objects.get_or_create(user=user)
    # return JsonResponse({
    #     "success": True,
    #     "user": model_to_dict(user, fields=["first_name", "last_name", "is_info_complete", "email", "username"])
    # })
    # # except:
    # #     return JsonResponse({
    # #         "success": False
    # #     })


def update_user(request):
    print(request.body)  # Debug
    try:
        d = json.loads(request.body)
        d["is_info_complete"] = True
        # print(d)  # Debug
        query = User.objects.filter(uid=d["uid"])

        query.update(**d)
        return JsonResponse({
            "success": True,
            "user": model_to_dict(query[0], fields=["first_name", "last_name", "is_info_complete", "email", "username", "birth_date"])
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })
