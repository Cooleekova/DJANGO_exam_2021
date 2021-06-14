"""django_diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from shop import views
from rest_framework.routers import DefaultRouter

from shop.views import UserViewSet

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('product-reviews', views.ReviewViewSet, basename='product-reviews')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('product-collections', views.CollectionViewSet, basename='product-collections')

router.register('all-profiles', UserViewSet, basename='all-profiles')
router.register('profile/<int:pk>', UserViewSet, basename='profile')


urlpatterns = router.urls
