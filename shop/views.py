from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, ReadOnly, IsAdminUser
from .models import Product, Review, Order, Collection
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer, UserSerializer
from .filters import ProductFilter, ReviewFilter, OrderFilter
from django.contrib.auth.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


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

    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        """Оставлять отзыв к товару могут только авторизованные пользователи."""
        """Пользователь может обновлять и удалять только свой собственный отзыв."""
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    """ Создавать заказы могут только авторизованные пользователи """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Админы могут получать все заказы, остальное пользователи только свои."""
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(creator=self.request.user)


class CollectionViewSet(ModelViewSet):

    """Создавать подборки могут только админы,
    остальные пользователи могут только их смотреть."""

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminUser | ReadOnly]


