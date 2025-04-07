from django.contrib import admin
from .models import Product, Size, Color, ProductGallery, TopMaterial, SoleMaterial, InsoleModel, OpenClose, Comment, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'price', 'discount_percentage', 'discounted_price', 'created_at', 'update_at')
    exclude = ('slug',)
    list_filter = ('created_at', 'update_at', 'discount_percentage')
    search_fields = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent',)
    search_fields = ('title',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)


@admin.register(TopMaterial)
class TopMaterialAdmin(admin.ModelAdmin):
    list_display = ('top_material',)


@admin.register(SoleMaterial)
class SoleMaterialAdmin(admin.ModelAdmin):
    list_display = ('sole_material',)


@admin.register(InsoleModel)
class InsoleModelAdmin(admin.ModelAdmin):
    list_display = ('insole_model',)


@admin.register(OpenClose)
class OpenCloseAdmin(admin.ModelAdmin):
    list_display = ('open_close',)


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text')


admin.site.register(Comment)