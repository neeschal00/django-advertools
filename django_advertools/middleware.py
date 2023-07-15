from django.template.response import TemplateResponse
# middleware.py
from django.conf import settings
from django.http import HttpResponse

class LoaderMiddleware(object):
    def __init__(self, get_response):
        print("LoaderMiddleware initialized")
        self.get_response = get_response

    def process_request(self, request):
        request.show_loader = True
        return None

    def process_template_response(self, request, response):
        if isinstance(response, TemplateResponse):
            response.context_data["show_loader"] = request.show_loader
            del request.show_loader
        return response



class CustomCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        if 'custom_cookie' not in request.COOKIES:
            response = HttpResponse()
            response.set_cookie('custom_cookie', 'cookie_value')
            return response

        return self.get_response(request)
