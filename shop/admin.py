from django.contrib import admin
from .models import Product, Review, Order, Collection


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('title', 'price',)
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
