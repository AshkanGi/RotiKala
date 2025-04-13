from django.contrib import admin
from .models import (Product, ProductGallery, Attribute, AttributeValue, Category, ProductAttribute,
                     ProductBooleanAttribute, BooleanAttribute, Comment, Like)


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    verbose_name = "تصویر گالری"
    verbose_name_plural = "تصاویر گالری"


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    verbose_name = "ویژگی"
    verbose_name_plural = "ویژگی‌ها"


class ProductBooleanAttributeInline(admin.TabularInline):
    model = ProductBooleanAttribute
    extra = 1
    verbose_name = "ویژگی"
    verbose_name_plural = "ویژگی‌ها"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_percentage', 'get_discounted_price', 'created_at', 'update_at']
    search_fields = ['name', 'slug']
    list_filter = ['category', 'created_at', 'discount_percentage']
    exclude = ('slug',)
    inlines = [ProductGalleryInline, ProductAttributeInline, ProductBooleanAttributeInline]
    filter_horizontal = ('category',)

    def get_discounted_price(self, obj):
        return obj.discounted_price
    get_discounted_price.short_description = "قیمت با تخفیف"


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(BooleanAttribute)
class BooleanAttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title']
    list_filter = ['parent']


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'image']
    search_fields = ['alt_text']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'create_at']
    search_fields = ['user', 'product']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'title', 'is_recommended', 'created_at']
    search_fields = ['user', 'product']
    list_filter = ['is_recommended']