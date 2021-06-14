from django.conf import settings
from django.db import models
from django.contrib import admin


class StandardFields(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Product(StandardFields):

    title = models.CharField(max_length=50)
    description = models.TextField(default='')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class GradeChoices(models.IntegerChoices):
    """Оценка объявления по шкале от 1 до 5"""

    TERRIBLE = 1, 'Ужос!'
    BAD = 2, 'Так себе'
    NORMAL = 3, 'Норм'
    GOOD = 4, 'Хорошо'
    EXCELLENT = 5, 'Отлично'


class Review(StandardFields):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Товар',
    )
    # select_related('product')

    description = models.TextField(
        blank=False,
        null=False,
    )

    grade = models.IntegerField(
        choices=GradeChoices.choices,
        verbose_name='Оценка',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class OrderStatus(models.TextChoices):
    """Статусы заказа."""

    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS", "В обработке"
    DONE = "DONE", "Закрыт"


class Order(StandardFields):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор заказа',
    )

    positions = models.ManyToManyField(
        'Product',
        related_name='orders',
        through='ProductsInOrder',
    )

    status = models.TextField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @admin.display(description='Количество товаров')
    def quantity(self):
        return int(self.positions.count())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductsInOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=1,
        blank=False,
        null=False,
    )

    def __str__(self):
        return '{0}_{1}'.format(self.order, self.product)


class Collection(StandardFields):

    title = models.TextField()
    description = models.TextField(
        default='',
        blank=False,
        null=False,
    )

    products = models.ManyToManyField(
        'Product',
        related_name='collections'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

