from django.urls import reverse
from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:    # بعد از لاگین به این صفحات دسترسی ندارید
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_urls = [
            reverse('account:check-username'),
            reverse('account:verify-otp'),
            reverse('account:login'),
            reverse('account:forget'),
            reverse('account:forget-verify-otp'),
            reverse('account:reset-password'),
            reverse('account:enter-otp'),
            reverse('account:enter-verify-otp'),
        ]

    def __call__(self, request):
        if request.user.is_authenticated and request.path in self.restricted_urls:
            return redirect('core:home')
        return self.get_response(request)