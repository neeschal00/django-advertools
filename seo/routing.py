from django.urls import re_path
from .consumers import TaskCompletionConsumer


websocket_urlpatterns = [
    re_path(r'ws/group/(?P<random_id>\w+)/$', TaskCompletionConsumer.as_asgi()),
]
