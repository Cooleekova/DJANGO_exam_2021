from django.contrib import admin
from .models import Product, Review, Order, Collection, ProductsInOrder


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 1


class ProductInline(admin.TabularInline):
    model = Collection.products.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'grade', 'creator',)


@admin.register(Order)
@admin.display(ordering='created_at')
class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'creator', 'created_at', 'quantity',)
    inlines = [ProductsInOrderInline]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    inlines = [ProductInline]
    exclude = ('products',)
