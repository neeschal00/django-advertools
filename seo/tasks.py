from celery import shared_task
import os
from ydata_profiling import ProfileReport
from django.contrib import messages
import pandas as pd
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
@shared_task
def generateReport(task_id,df,minimal=False,title="Profile Report"):
    # messages.warning("Report generation on progress wait for completion")
    print(title +" "+ str(minimal))
    load_df = pd.read_json(df)
    try:
        if minimal:
            profile = ProfileReport(load_df,minimal=True,title=title)
        else:
            profile = ProfileReport(load_df,minimal=False,title=title)
        profile.to_file(os.path.join('templates',"report.html"))
        # messages.success("Report Has been generated sucessfully")
        
        async_to_sync(channel_layer.group_send)(
            f'task_{task_id}',
            {
                'type': 'task_completed',
                'result': 'Task completed successfully.'
            }
        )
        return "Report Has been generated successfully"
    except Exception as e:
        print(e)
        return "Report was not generated"


@shared_task
def add(a,b):
    return a+b
