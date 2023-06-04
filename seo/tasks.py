from celery import shared_task
import os
from ydata_profiling import ProfileReport
import pandas as pd
from django_advertools.celery import app
import time


@shared_task
def generateReport(df,minimal=False,title="Profile Report"):
    print(df)
    print(os.path.join('templates',"report.html"))
    # load_df = pd.read_json(df)
    # # try:
    # profile = ProfileReport(load_df,minimal=minimal,title=title)
    # profile.to_file(os.path.join('templates',"report.html"))
    time.sleep(8)
    return df
    # except Exception as e:
    #     print(e)
    #     return False

@shared_task
def add(a,d):
    return int(a)+ int(d)