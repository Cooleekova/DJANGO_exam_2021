from django.contrib import admin
from .models import Product, Review, Order, Collection, ProductsInOrder


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'grade', 'creator',)


@admin.register(Order)
@admin.display(ordering='created_at')
class OrderAdmin(admin.ModelAdmin):
    list_display = ('creator', 'created_at', 'quantity',)
    inlines = [ProductsInOrderInline]

    """Менять статус заказа могут только админы."""
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('status')
        return fields


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
