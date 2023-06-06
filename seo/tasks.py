from celery import shared_task
import os
from ydata_profiling import ProfileReport
import pandas as pd

@shared_task
def generateReport(df,minimal=False,title="Profile Report"):
    load_df = pd.read_json(df)
    try:
        profile = ProfileReport(load_df,minimal=minimal,title=title)
        profile.to_file(os.path.join('templates',"report.html"))
        return True
    except Exception as e:
        print(e)
        return False


@shared_task
def add(a,b):
    return a+b
