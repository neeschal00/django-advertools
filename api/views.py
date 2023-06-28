from django.http import JsonResponse
from celery.result import AsyncResult
from analyse.models import DatasetFile
import pandas as pd


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


def getCsvColumns(request, pid):
    dataset = DatasetFile.objects.get(id=pid)
    csv_path = dataset.file_field
    print(csv_path)
    try:
        csv_file = pd.read_csv(csv_path)
        header = csv_file.columns.to_list()
        return JsonResponse({"result": header})
    except Exception as e:
        return JsonResponse({"result": []})
