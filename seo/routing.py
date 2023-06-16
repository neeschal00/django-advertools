from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/task/(?P<task_id>\w+)/$', consumers.TaskCompletionConsumer.as_asgi()),
]
