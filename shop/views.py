from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsOwnerOrReadOnly, ReadOnly
from .models import Product, Review, Order, Collection
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer
from .filters import ProductFilter, ReviewFilter, OrderFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [IsAdminUser]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    # Before running the main body of the view each permission in the list is checked.
    """Оставлять отзыв к товару могут только авторизованные пользователи."""
    """Пользователь может обновлять и удалять только свой собственный отзыв."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    """ Создавать заказы могут только авторизованные пользователи """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Админы могут получать все заказы, остальное пользователи только свои."""
        if self.request.user.is_stuff:
            return self.request.order.objects.all()
        else:
            return self.request.order.objects.filter(creator=self.request.user)

    """Менять статус заказа могут только админы."""
    # здесь нужно написать логику


class CollectionViewSet(ModelViewSet):

    """Создавать подборки могут только админы,
    остальные пользователи могут только их смотреть."""

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminUser | ReadOnly]


