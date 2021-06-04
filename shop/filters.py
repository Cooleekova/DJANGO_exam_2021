from django_filters import rest_framework as filters
from .models import Product, Review, Order


class ProductFilter(filters.FilterSet):
    """Фильтр для товаров."""
    """ по цене и содержимому из названия / описания"""

    # здесь нужно прописать логику для фильтра

    class Meta:
        model = Product
        fields = ['price', 'title', 'description']


class ReviewFilter(filters.FilterSet):
    """Фильтр для отзывов к товарам."""
    """ по ID пользователя, дате создания и ID товара """

    class Meta:
        model = Review
        fields = ['creator', 'created_at', 'product']


# Заказы можно фильтровать
class OrderFilter(filters.FilterSet):
    """Фильтр для заказов."""
    """ по статусу / общей сумме / дате создания / дате обновления и продуктам из позиций."""

    # здесь нужно прописать логику для фильтра
    # Order.objects.filter(positions__product__''''')

    class Meta:
        model = Order
        fields = [
            'status',
            'total_amount',
            'created_at',
            'updated_at',
            'positions'
        ]



