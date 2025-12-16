from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVideo


admin.site.site_header = "Bablu Printing Press Admin"
admin.site.site_title = "Bablu Printing Press"
admin.site.index_title = "Administration Panel"
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVideoInline]
