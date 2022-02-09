import json
from django.http import JsonResponse
# Create your views here.
# from .models import Version

# latest_v=Version.objects.get(is_latest=True)

# def version_check(request):
#     #request_post = request.POST.dict()
#     print(request.body)
#     d=json.loads(request.body)
    
#     if latest_v.version_int>int(d.get('version').replace('.','')):
#         if latest_v.update_required :  
#             return JsonResponse(dict(success=True, newer_version_exists=True, update_required=True))
#         else:
#             return JsonResponse(dict(success=True, newer_version_exists=True, update_required=False))
#     return JsonResponse(dict(success=True, newer_version_exists=False))    
