import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN


# проверка получения одной подборки
@pytest.mark.django_db
def test_get_collection(client, collection_factory):
    # создаём одну коллекцию
    collection = collection_factory()
    url = reverse("product-collections-list")
    # совершаем запрос GET к API по URL
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json
    test_collection = resp_json[0]
    # проверяем, что вернулась именно та коллекция, которую запрашивали
    assert test_collection['title'] == collection.title


# проверка получения списка подборок
@pytest.mark.django_db
def test_get_collections_list(client, collection_factory):
    # создаём десять коллекций
    collection_factory(_quantity=10)
    url = reverse("product-collections-list")
    # совершаем запрос GET к API по URL
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json
    # проверяем, что вернувшийся json содержит десять записей
    assert len(resp_json) == 10


# тест успешного создания подборки админом
@pytest.mark.django_db
def test_admin_can_create_new_collection(admin_test_client, product_factory):
    # создаём продукт для добавления в коллекцию
    test_product = product_factory()
    product_id = test_product.id
    # создаём коллекцию
    url = reverse("product-collections-list")
    new_test_collection = {
        'title': 'TEST 12345',
        'products': product_id,
    }
    # совершаем запрос POST к API по URL
    resp = admin_test_client.post(url, new_test_collection)
    # проверяем код ответа,
    # если коллекция создана успешно, код будет 201
    assert resp.status_code == HTTP_201_CREATED


# тест безуспешного создания подборки НЕ админом
@pytest.mark.django_db
def test_user_cannot_create_new_collection(auth_client, product_factory):
    # создаём продукт для добавления в коллекцию
    test_product = product_factory()
    product_id = test_product.id
    # создаём коллекцию
    url = reverse("product-collections-list")
    new_test_collection = {
        'title': 'TEST 12345',
        'products': product_id,
    }
    # совершаем запрос POST к API по URL
    resp = auth_client.post(url, new_test_collection)
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 403 (нет доступа)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест успешного изменения подборки админом
@pytest.mark.django_db
def test_admin_can_update_collection(admin_test_client, product_factory):
    # создаём продукт для добавления в коллекцию
    test_product = product_factory()
    product_id = test_product.id
    # создаём коллекцию
    title = 'TEST 12345'
    url = reverse("product-collections-list")
    new_test_collection = {
        'title': title,
        'products': product_id,
    }
    admin_test_client.post(url, new_test_collection)
    resp2 = admin_test_client.get(url, {'title': title})
    resp2_json = resp2.json()
    collection_id = resp2_json[0]['id']
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'title': 'UPDATED COLLECTION TITLE'
    }
    # совершаем запрос PATCH к API по URL

    collection_url = reverse("product-collections-detail", args=[collection_id])
    resp3 = admin_test_client.patch(collection_url, updated_info)
    # проверяем код ответа,
    # если коллекция изменена успешно, код будет 200 ОК
    assert resp3.status_code == HTTP_200_OK


# тест безуспешного изменения подборки НЕ админом
def test_user_cannot_update_collection(auth_client, collection_factory):
    # создаём коллекцию
    test_collection = collection_factory(make_m2m=True)
    collection_id = test_collection.id

    # создаём словарь с небходимыми изменениями
    updated_info = {
        'title': 'UPDATED COLLECTION TITLE'
    }
    # совершаем запрос PATCH к API по URL
    collection_url = reverse("product-collections-detail", args=[collection_id])
    resp = auth_client.patch(collection_url, updated_info)
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 403 (нет доступа)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест успешного удаления подборки админом
@pytest.mark.django_db
def test_admin_can_delete_collection(admin_test_client, collection_factory):
    # создаём коллекцию
    test_collection = collection_factory(make_m2m=True)
    collection_id = test_collection.id

    # совершаем запрос DELETE к API по URL

    collection_url = reverse("product-collections-detail", args=[collection_id])
    resp = admin_test_client.delete(collection_url)
    # проверяем код ответа,
    # если коллекция удалена успешно, код будет 204
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест безуспешного удаления подборки НЕ админом
@pytest.mark.django_db
def test_user_cannot_delete_collection(auth_client, collection_factory):
    # создаём коллекцию
    test_collection = collection_factory(make_m2m=True)
    collection_id = test_collection.id

    # совершаем запрос PATCH к API по URL
    collection_url = reverse("product-collections-detail", args=[collection_id])
    resp = auth_client.delete(collection_url)
    # проверяем код ответа,
    # если коллекция создана успешно, код будет 200 ОК
    assert resp.status_code == HTTP_403_FORBIDDEN

