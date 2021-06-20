from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Review, Order, Collection


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id', 'username', 'first_name',
        #           'last_name',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ['id', 'creator', 'product', 'description', 'grade', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """ Метод для валидации."""
        """ 1 пользователь не может оставлять более 1го отзыва."""

        creator = self.context["request"].user
        product = data["product"]
        review_quantity = Review.objects.filter(creator=creator.id, product=product).count()
        if self.context["request"].method == "POST" and review_quantity >= 1:
            raise serializers.ValidationError(f'You already posted review for this product')
        else:
            return data


class OrderSerializer(serializers.ModelSerializer):

    # status = serializers.ChoiceField(choices=Order.OrderStatus.choices, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'creator', 'positions', 'status', 'total_amount', 'created_at', 'updated_at']
        # read_only_fields = ['status']

    def create(self, validated_data):
        """Метод для создания заказа"""
        # Простановка значения поля создатель по-умолчанию.
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    """Менять статус заказа могут только админы."""
    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.is_superuser:
            return super(OrderSerializer, self).update(instance, validated_data)
        else:
            fields = instance._meta.fields
            exclude = ['status']
            for field in fields:
                field = field.name.split('.')[-1]
                if field in exclude:
                    continue
                exec("instance.%s = validated_data.get(field, instance.%s)" % (field, field))
            instance.save()
            return instance


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'description', 'products', 'created_at', 'updated_at']


