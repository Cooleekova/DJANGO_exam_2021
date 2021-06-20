import decimal
import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN


# проверка получения одного товара
@pytest.mark.django_db
def test_get_product(auth_client, product_factory):
    # создаём товар
    test_product = product_factory(make_m2m=True)
    product_id = test_product.id
    url = reverse("products-list")
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    # проверяем, что вернулся тот продукт, который мы запрашивали
    test_product = resp_json[0]
    assert test_product['id'] == product_id


# проверка получения списка товаров авторизованным пользователем
@pytest.mark.django_db
def test_auth_user_gets_products(auth_client, product_factory):
    # создаём товары
    quantity = 30
    product_factory(make_m2m=True, _quantity=quantity)
    url = reverse("products-list")
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    resp_json = resp.json()
    # проверяем, что все товары показаны пользователю
    assert len(resp_json) == quantity
    # проверяем код ответа, дожен быть 200 ОК
    assert resp.status_code == HTTP_200_OK


# проверка получения списка товаров НЕ авторизованным пользователем
@pytest.mark.django_db
def test_not_auth_user_gets_products(client, product_factory):
    # создаём товары
    quantity = 30
    product_factory(make_m2m=True, _quantity=quantity)
    url = reverse("products-list")
    # совершаем запрос GET к API по URL
    resp = client.get(url)
    resp_json = resp.json()
    # проверяем, что все товары показаны пользователю
    assert len(resp_json) == quantity
    # проверяем код ответа, дожен быть 200 ОК
    assert resp.status_code == HTTP_200_OK


# тест успешного создания товара Админом
@pytest.mark.django_db
def test_admin_can_create_new_product(admin_test_client, product_factory):
    # создаём продукт
    url = reverse("products-list")
    new_test_product = {
        'title': 'new_test_product-new_test_product',
        'price': 100.00,
    }
    # совершаем запрос POST к API по URL
    resp = admin_test_client.post(url, new_test_product)
    # проверяем код ответа,
    # если продукт создан успешно, код будет 201
    assert resp.status_code == HTTP_201_CREATED


# тест безуспешного создания товара НЕ админом
@pytest.mark.django_db
def test_user_cannot_create_new_product(auth_client, product_factory):
    # создаём продукт
    url = reverse("products-list")
    new_test_product = {
        'title': 'new_test_product-new_test_product',
        'price': 100.00,
    }
    # совершаем запрос POST к API по URL
    resp = auth_client.post(url, new_test_product)
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 403 (нет доступа)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест успешного изменения товара Админом
def test_admin_can_update_product(admin_test_client, product_factory):
    # создаём товар
    test_product = product_factory(make_m2m=True)
    # получаем id товара
    product_id = test_product.id
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'title': 'NEW TEST PRODUCT TITLE'
    }
    # совершаем запрос PATCH к API по URL
    product_url = reverse("products-detail", args=[product_id])
    resp = admin_test_client.patch(product_url, updated_info)
    updated_product = resp.json()
    # проверяем код ответа,
    # если заказ изменён успешно, код будет 200 ОК
    assert resp.status_code == HTTP_200_OK
    assert updated_product['title'] == updated_info['title']


# тест безуспешного изменения товара НЕ Админом
def test_user_cannot_update_product(auth_client, product_factory):
    # создаём товар
    test_product = product_factory(make_m2m=True)
    # получаем id товара
    product_id = test_product.id
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'title': 'NEW TEST PRODUCT TITLE'
    }
    # совершаем запрос PATCH к API по URL
    product_url = reverse("products-detail", args=[product_id])
    resp = auth_client.patch(product_url, updated_info)
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 403 (нет доступа)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест успешного удаления товара Админом
def test_admin_can_delete_product(admin_test_client, product_factory):
    # создаём товар
    test_product = product_factory(make_m2m=True)
    # получаем id товара
    product_id = test_product.id
    # совершаем запрос DELETE к API по URL
    product_url = reverse("products-detail", args=[product_id])
    resp = admin_test_client.delete(product_url)
    # проверяем код ответа,
    # если товар удалён успешно, код будет 204
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест БЕЗуспешного удаления товара НЕ Админом
def test_user_cannot_delete_product(auth_client, product_factory):
    # создаём товар
    test_product = product_factory(make_m2m=True)
    # получаем id товара
    product_id = test_product.id
    # совершаем запрос DELETE к API по URL
    product_url = reverse("products-detail", args=[product_id])
    resp = auth_client.delete(product_url)
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 403 (нет доступа)
    assert resp.status_code == HTTP_403_FORBIDDEN


''' фильтрация '''


# проверка фильтрации товаров:
# по цене
@pytest.mark.django_db
def test_filter_product_price(auth_client, product_factory):
    # создаём товар
    price = decimal.Decimal(12345.00)
    product_factory(make_m2m=True, price=price)
    # прописываем в URL цену, по которой будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    url = reverse("products-list")
    resp = auth_client.get(url, {'price': price})
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert decimal.Decimal(resp_json[0]['price']) == price


# проверка фильтрации товаров:
# по содержимому из названия
def test_filter_product_title(auth_client, product_factory):
    # создаём товар
    title = 'FirstSecondThirdWord'
    product_factory(make_m2m=True, title=title)
    part_of_title = title[3:8]
    # прописываем в URL статус, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    url = reverse("products-list")
    resp = auth_client.get(url, {'title': title})
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['title'] == title
    resp2 = auth_client.get(url, {'title': part_of_title})
    resp2_json = resp2.json()
    assert resp2.status_code == HTTP_200_OK
    assert part_of_title in resp2_json[0]['title']


# проверка фильтрации товаров:
# по содержимому из описания
def test_filter_product_description(auth_client, product_factory):
    # создаём товар
    description = 'FirstSecondThirdWord FourthFifthSixSeventhEightsNinthTens'
    product_factory(make_m2m=True, description=description)
    part_of_description = description[10:20]
    # прописываем в URL статус, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    url = reverse("products-list")
    resp = auth_client.get(url, {'description': description})
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['description'] == description
    resp2 = auth_client.get(url, {'description': part_of_description})
    resp2_json = resp2.json()
    assert resp2.status_code == HTTP_200_OK
    assert part_of_description in resp2_json[0]['description']
