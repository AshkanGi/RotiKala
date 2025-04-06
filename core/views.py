from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, 'core/index.html')


class FaqView(View):
    def get(self, request):
        return render(request, 'core/faq.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'core/about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'core/contact.html')


class WhyUsView(View):
    def get(self, request):
        return render(request, 'core/why-us.html')


class HowToBuyView(View):
    def get(self, request):
        return render(request, 'core/how-to-buy.html')