from django.contrib import admin

# Register your models here.
from .models import Product, ProductLike

class ProductLikeAdmin(admin.TabularInline):
    model = ProductLike

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user_username', 'user_email']
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)