from django.contrib import admin
from .models import Address, OrderItem, Order, DiscountCode


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'total_price')
    readonly_fields = ('created_at',)
    inlines = [OrderItemAdmin]
    ordering = ('-created_at',)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'discount')
    search_fields = ('name',)
    list_filter = ('discount',)
    ordering = ('-discount',)
    prepopulated_fields = {'name': ('name',)}


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'province', 'city', 'phone')
    search_fields = ('user__username', 'phone', 'province', 'city')
    list_filter = ('province', 'city')
