import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework.authtoken.admin import User
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.authtoken.models import Token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db, client):
    data = {
        "email": "egg@mail.com",
        "username": "Egg",
        "password": "egg1988Y"
    }
    response = client.post('/auth/users/', data)
    response_json = response.json()
    assert response_json['username'] == data['username']
    assert response.status_code == HTTP_201_CREATED
    user = User.objects.get(username="Egg")
    return user


@pytest.fixture
def token(db, client, user):
    Token.objects.create(user=user)
    token = Token.objects.get(user=user)
    return token


@pytest.fixture
def auth_client(db, client, user, token):

    client.force_authenticate(user=user, token=token)
    return client


@pytest.fixture
def admin_token(db, client, admin_user):
    Token.objects.create(user=admin_user)
    token = Token.objects.get(user=admin_user)
    return token


@pytest.fixture
def admin_test_client(db, client, admin_user, admin_token):

    client.force_authenticate(user=admin_user, token=admin_token)
    return client


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    return factory


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make('Collection', **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make('Review', **kwargs)
    return factory

