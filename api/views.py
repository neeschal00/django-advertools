from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from celery.result import AsyncResult
# from seo.tasks import 
# Create your views here.

def getMainTaskResponse(request,task_id):

    task_resp = AsyncResult(id=task_id)
    if task_resp.state == "SUCCESS":
        data = task_resp.get() 
        return JsonResponse(
                data
        )
    else:
        return JsonResponse({
            "error": "task failed"
        }
        )

def getAnalysisTaskResponse(request,task_id):

    task_resp = AsyncResult(id=task_id)
    if task_resp.state == "SUCCESS":
        data = task_resp.get() 
        return JsonResponse(
                data
        )
    else:
        return JsonResponse({
            "error": "task failed"
        }
        )

