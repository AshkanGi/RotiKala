from django.contrib import admin
from .models import Product, ProductGallery, Attribute, AttributeValue, Category, ProductAttribute, Comment, Like


class ProductGalleryInline(admin.TabularInline):
    model = Product.gallery_image.through
    extra = 1
    verbose_name = "تصویر گالری"
    verbose_name_plural = "تصاویر گالری"


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    verbose_name = "ویژگی"
    verbose_name_plural = "ویژگی‌ها"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percentage', 'discounted_price', 'created_at']
    search_fields = ['name', 'slug']
    list_filter = ['category', 'created_at']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductGalleryInline, ProductAttributeInline]
    filter_horizontal = ('category', 'gallery_image')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
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


admin.site.register(Comment)
admin.site.register(Like)