from django.urls import re_path
from .consumers import TaskCompletionConsumer


websocket_urlpatterns = [
    re_path(r'ws/task/(?P<task_id>\w+)/$', TaskCompletionConsumer.as_asgi()),
]
