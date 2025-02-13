import json
from django.http import JsonResponse
from django.db import IntegrityError


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, IntegrityError):
            response_data = {
                "error": "Integrity error occurred.",
                "message": str(exception),
            }
            return JsonResponse(response_data, status=400)
        return None
