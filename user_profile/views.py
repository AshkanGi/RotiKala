from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request):
        return render(request, 'user_profile/dashboard.html')


class OrdersView(View):
    def get(self, request):
        return render(request, 'user_profile/order.html')


class FavoritesView(View):
    def get(self, request):
        return render(request, 'user_profile/favorite.html')


class RecentView(View):
    def get(self, request):
        return render(request, 'user_profile/recent.html')


class NotificationView(View):
    def get(self, request):
        return render(request, 'user_profile/notification.html')


class AddressView(View):
    def get(self, request):
        return render(request, 'user_profile/address.html')


class EditView(View):
    def get(self, request):
        return render(request, 'user_profile/edite.html')