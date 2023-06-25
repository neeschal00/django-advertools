from django.http import JsonResponse
from celery.result import AsyncResult


def getMainTaskResponse(request, task_id):
    task_resp = AsyncResult(id=task_id)
    if task_resp.state == "SUCCESS":
        data = task_resp.get()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "task failed or task-id Not found"}, status=404)


def getAnalysisTaskResponse(request, task_id):
    task_resp = AsyncResult(id=task_id)
    if task_resp.state == "SUCCESS":
        data = task_resp.get()
        return JsonResponse(data)
    else:
        return JsonResponse(
            {"error": "task failed task failed or task-id Not found"}, status=404
        )
