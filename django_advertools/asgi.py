import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import seo.routing  # Replace 'myapp' with the name of your app
# from a2wsgi import ASGIMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_advertools.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(seo.routing.websocket_urlpatterns),
    }
)
# application = ASGIMiddleware(application)
