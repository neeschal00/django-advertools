from django.template.response import TemplateResponse
# middleware.py
from django.conf import settings
import uuid

# class LoaderMiddleware(object):
#     def __init__(self, get_response):
#         print("LoaderMiddleware initialized")
#         self.get_response = get_response

#     def process_request(self, request):
#         request.show_loader = True
#         return None

#     def process_template_response(self, request, response):
#         if isinstance(response, TemplateResponse):
#             response.context_data["show_loader"] = request.show_loader
#             del request.show_loader
#         return response



class CustomCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'socket_id' not in request.COOKIES:
            response = self.get_response(request)
            socket_id = uuid.uuid4()
            response.set_cookie('socket_id',str(socket_id))
            return response
        return self.get_response(request)
