from django_filters import rest_framework as filters, ChoiceFilter, DateFromToRangeFilter, RangeFilter, CharFilter
from shop.models import Product, Review, Order, OrderStatus


class ProductFilter(filters.FilterSet):
    """Фильтр для товаров."""
    """ по цене и содержимому из названия / описания"""

    price = RangeFilter(field_name='price')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'price',
            'title',
            'description',
        ]


class ReviewFilter(filters.FilterSet):
    """Фильтр для отзывов к товарам."""
    """ по ID пользователя, дате создания и ID товара """

    created = DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Review
        fields = ['creator', 'created_at', 'product']


# Заказы можно фильтровать
class OrderFilter(filters.FilterSet):
    """Фильтр для заказов."""
    """ по статусу / общей сумме / дате создания / дате обновления и продуктам из позиций."""

    status = ChoiceFilter(choices=OrderStatus.choices)
    total_amount = RangeFilter(field_name='total_amount')
    created = DateFromToRangeFilter(field_name='created_at')
    updated = DateFromToRangeFilter(field_name='updated_at')
    products = filters.CharFilter(field_name='productsinorder__product__title',
                                  lookup_expr='icontains'
                                  )

    class Meta:
        model = Order
        fields = [
            'status',
            'total_amount',
            'created_at',
            'updated_at',
            'positions',
        ]
