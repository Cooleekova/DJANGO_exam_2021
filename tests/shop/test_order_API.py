import decimal
import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


# проверка получения одного заказа
@pytest.mark.django_db
def test_get_order(user, auth_client, order_factory):
    # создаём заказ
    order_factory(make_m2m=True)

    test_amount = decimal.Decimal(12435.00)
    url = reverse("orders-list")
    new_test_order = {
        'total_amount': test_amount,
        'creator': user.id,
    }
    # совершаем запрос POST к API по URL
    response = auth_client.post(url, new_test_order)
    created_order = response.json()
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    # проверяем, что вернулся тот заказ, который мы запрашивали
    test_order = resp_json[0]
    assert test_order['id'] == created_order['id']


# проверка получения полного списка заказов админом
@pytest.mark.django_db
def test_admin_gets_all_orders(user, admin_test_client, order_factory):
    # создаём заказы, используя тестового пользователя user
    order_factory(_quantity=20, make_m2m=True, creator=user)
    url = reverse("orders-list")

    # совершаем запрос GET к API по URL
    resp = admin_test_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 20


# проверка НЕ получения списка ВСЕХ заказов НЕ админом
@pytest.mark.django_db
def test_user_cannot_get_all_orders(auth_client, order_factory):
    # создаём заказы
    order_factory(_quantity=20, make_m2m=True)
    url = reverse("orders-list")

    # совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 0


# проверка получения пользователем списка своих заказов
@pytest.mark.django_db
def test_user_cannot_get_all_orders(user, auth_client, order_factory):
    # создаём заказы
    order_factory(_quantity=5, make_m2m=True, creator=user)
    url = reverse("orders-list")

    # совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 5


# проверка НЕ получения пользователем ЧУЖИХ заказов
@pytest.mark.django_db
def test_user_cannot_get_other_users_orders(auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True)
    # получаем id заказа
    order_id = test_order.id
    url = reverse("orders-detail", args=[order_id])
    # используя полученный id, совершаем запрос GET к API по URL
    resp = auth_client.get(url)
    assert resp.status_code == HTTP_404_NOT_FOUND


# тест успешного создания заказа авторизованным пользователем
@pytest.mark.django_db
def test_auth_user_can_create_order(user, auth_client):
    # создаём заказ
    test_amount = decimal.Decimal(12435.00)
    url = reverse("orders-list")
    new_test_order = {
        'total_amount': test_amount,
        'creator': user.id,
    }
    # совершаем запрос POST к API по URL
    resp = auth_client.post(url, new_test_order)
    resp_json = resp.json()
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 201
    assert resp.status_code == HTTP_201_CREATED
    assert decimal.Decimal(resp_json['total_amount']) == test_amount


# тест безуспешного создания заказа НЕ авторизованным пользователем
def test_not_auth_user_cannot_create_order(user, client, order_factory):
    # создаём заказ
    test_amount = decimal.Decimal(12435.00)
    url = reverse("orders-list")
    new_test_order = {
        'total_amount': test_amount,
        'creator': user.id,
    }
    # совершаем запрос POST к API по URL
    resp = client.post(url, new_test_order)
    # проверяем код ответа,
    # если разрешения нстроены правильно, код будет 401
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# тест успешного изменения заказа
@pytest.mark.django_db
def test_user_can_update_order(user, auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True, creator=user)
    # получаем id заказа
    order_id = test_order.id
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'total_amount': '1111.99'
    }

    # совершаем запрос PATCH к API по URL
    order_url = reverse("orders-detail", args=[order_id])
    resp = auth_client.patch(order_url, updated_info)
    updated_order = resp.json()
    # проверяем код ответа,
    # если заказ изменён успешно, код будет 200 ОК
    assert resp.status_code == HTTP_200_OK
    assert updated_order['total_amount'] == updated_info['total_amount']


# тест успешного удаления заказа пользователем
def test_user_can_delete_his_order(user, auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True, creator=user)
    # получаем id заказа
    order_id = test_order.id
    # совершаем запрос DELETE к API по URL
    order_url = reverse("orders-detail", args=[order_id])
    resp = auth_client.delete(order_url)
    # проверяем код ответа,
    # если заказ удалён успешно, код будет 204
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест успешного изменения СТАТУСА заказа админом
def test_admin_can_change_status(admin_test_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True)
    # получаем id и статус заказа
    order_id = test_order.id
    # order_status = order[0].status
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'status': 'DONE'
    }

    # совершаем запрос PATCH к API по URL
    order_url = reverse("orders-detail", args=[order_id])
    resp = admin_test_client.patch(order_url, updated_info)
    updated_order = resp.json()
    # проверяем код ответа,
    # статус должен измениться
    assert updated_order['status'] == updated_info['status']


# тест безуспешного изменения статуса заказа НЕ админом
def test_user_cannot_change_status(user, auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True, creator=user)
    # получаем id заказа
    order_id = test_order.id
    order_status = test_order.status
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'status': 'DONE'
    }

    # совершаем запрос PATCH к API по URL
    order_url = reverse("orders-detail", args=[order_id])
    resp = auth_client.patch(order_url, updated_info)
    updated_order = resp.json()
    # проверяем код ответа,
    # статус должен остаться прежним
    assert updated_order['status'] == order_status


''' фильтрация '''


# проверка фильтрации списка заказов:
# по статусу
@pytest.mark.django_db
def test_filter_order_status(user, auth_client, order_factory):
    # создаём заказ
    status = 'DONE'
    order_factory(make_m2m=True, creator=user, status=status)

    url = reverse("orders-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация

    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'status': status})
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['status'] == status


# проверка фильтрации списка заказов:
# по общей сумме
@pytest.mark.django_db
def test_filter_order_amount(user, auth_client, order_factory):
    # создаём заказ
    total_amount = decimal.Decimal(12345.00)
    order_factory(make_m2m=True, creator=user, total_amount=total_amount)

    url = reverse("orders-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация

    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'total_amount': total_amount})
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert decimal.Decimal(resp_json[0]['total_amount']) == total_amount


# проверка фильтрации списка заказов:
# по дате создания
@pytest.mark.django_db
def test_filter_order_created_date(user, auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True)
    # получаем дату создания заказа
    created_date = test_order.created_at

    url = reverse("orders-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация

    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'created_at': created_date})
    assert resp.status_code == HTTP_200_OK


# проверка фильтрации списка заказов:
# по дате обновления
def test_filter_order_products(user, auth_client, order_factory):
    # создаём заказ
    test_order = order_factory(make_m2m=True, creator=user)
    # из заказа получаем название и id продукта из первой позиции
    product_name = test_order.positions.all()[0].title
    product_id = test_order.positions.all()[0].id
    url = reverse("orders-list")
    # прописываем в URL продукт, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    resp = auth_client.get(
        url,
        {'products': product_name}
    )
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    # проверяем, что список позиций заказа модержит нужный продукт
    assert product_id in resp_json[0]['positions']
