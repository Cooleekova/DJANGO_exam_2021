import pytest
from pytest_django.fixtures import admin_client, admin_user
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework.authtoken.admin import User


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def test_client(db, client):
        data = {
            "email": "egg@mail.com",
            "username": "Egg",
            "password": "egg1988Y"
        }
        response = client.post('/auth/users/', data)
        resp_json = response.json()
        assert resp_json['username'] == data['username']
        # assert response.status_code == HTTP_201_CREATED

        # url_token = reverse('/auth/jwt/create/')
        response2 = client.post('/auth/jwt/create/', data={"username": "Egg", "password": "egg1988Y"})
        assert response2.data['access']
        token = response2.data['access']
        client.force_authenticate()
        return client


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user









# @pytest.fixture
# def a_client():
#     username = 'fred'
#     password = 'sec54b5hhyjv6/ret'
#     user = User.objects.create_user(username=username, password=password)
#     a = APIClient()
#     a.login(username=username, password=password)
#     return a

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

