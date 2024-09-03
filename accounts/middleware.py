from typing import Any
from django.shortcuts import redirect
from django.urls import reverse


class RedirectIfNotLoggedInMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/':
            return redirect('home')

        response = self.get_response(request)
        return response
