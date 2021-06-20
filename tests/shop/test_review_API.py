import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT


# проверка получения списка отзывов
@pytest.mark.django_db
def test_review_list(client, review_factory):
    # создаём десять отзывов
    review_factory(_quantity=10)
    url = reverse("product-reviews-list")
    # совершаем запрос GET к API по URL
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    # проверяем, что вернувшийся json содержит десять записей
    assert len(resp_json) == 10


# тест успешного создания отзыва авторизованным пользователем
@pytest.mark.django_db
def test_auth_user_can_create_review(user, auth_client, product_factory):
    # создаём продукт, к которому будет создан отзыв
    test_product = product_factory()
    product_id = test_product.id
    # создаём отзыв
    new_test_review = {
        'creator': user.id,
        'description': 'TEST 12345',
        'product': product_id,
        'grade': 2,
    }
    url = reverse("product-reviews-list")
    # совершаем запрос POST к API по URL
    resp = auth_client.post(url, new_test_review)
    resp_json = resp.json()
    # проверяем код ответа,
    # если разрешения настроены правильно, код будет 201
    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['description'] == new_test_review['description']


# тест безуспешного создания пользователем второго отзыва
@pytest.mark.django_db
def test_auth_user_cannot_create_second_review(user, auth_client, product_factory):
    # создаём продукт, к которому будет создан отзыв
    test_product = product_factory()
    product_id = test_product.id
    # создаём отзыв
    new_test_review = {
        'creator': user.id,
        'description': 'TEST 12345',
        'product': product_id,
        'grade': 2,
    }
    url = reverse("product-reviews-list")
    # совершаем запрос POST к API по URL
    auth_client.post(url, new_test_review)

    # создаём второй отзыв на тот же продукт
    second_test_review = {
        'creator': user.id,
        'description': 'TEST 12345',
        'product': product_id,
        'grade': 5,
    }
    # совершаем ещё один запрос POST к API по URL
    resp = auth_client.post(url, second_test_review)
    resp_json = resp.json()
    # проверяем код ответа,
    # если разрешения настроены правильно, вернётся код 400
    assert resp_json['non_field_errors']
    assert resp.status_code == HTTP_400_BAD_REQUEST


# тест безуспешного создания отзыва НЕ авторизованным пользователем
@pytest.mark.django_db
def test_not_auth_user_cannot_create_review(user, client, product_factory):
    # создаём продукт, к которому будет создан отзыв
    test_product = product_factory()
    product_id = test_product.id
    # создаём отзыв
    new_test_review = {
        'creator': user.id,
        'description': 'TEST 12345',
        'product': product_id,
        'grade': 2,
    }
    url = reverse("product-reviews-list")
    # совершаем запрос POST к API по URL
    resp = client.post(url, new_test_review)
    # если разрешения нстроены правильно, код будет 401
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# тест успешного изменения своего отзыва пользователем
@pytest.mark.django_db
def test_user_can_update_review(user, auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True, creator=user)
    # получаем id отзыва
    review_id = test_review.id
    product_id = test_review.product.id
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'grade': 5,
        'description': '!!!new review description!!!',
        'product': product_id,
    }

    # совершаем запрос PATCH к API по URL
    review_url = reverse("product-reviews-detail", args=[review_id])
    resp = auth_client.patch(review_url, updated_info)
    updated_review = resp.json()
    # проверяем код ответа,
    # если заказ изменён успешно, код будет 200 ОК
    assert resp.status_code == HTTP_200_OK
    assert updated_review['grade'] == updated_info['grade']
    assert updated_review['description'] == updated_info['description']


# тест безуспешного изменения чужого отзыва пользователем
@pytest.mark.django_db
def test_user_cannot_update_other_user_review(user, auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True)
    # получаем id отзыва
    review_id = test_review.id
    product_id = test_review.product.id
    # создаём словарь с небходимыми изменениями
    updated_info = {
        'grade': 5,
        'description': '!!!new review description!!!',
        'product': product_id,
    }

    # совершаем запрос PATCH к API по URL
    review_url = reverse("product-reviews-detail", args=[review_id])
    resp = auth_client.patch(review_url, updated_info)
    # проверяем код ответа,
    # должен вернуться код 403
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест успешного удаления отзыва пользователем
def test_user_can_delete_his_review(user, auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True, creator=user)
    # получаем id отзыва
    review_id = test_review.id
    # совершаем запрос DELETE к API по URL
    review_url = reverse("product-reviews-detail", args=[review_id])
    resp = auth_client.delete(review_url)
    # проверяем код ответа,
    # если отзыв удалён успешно, код будет 204
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест безуспешного удаления чужого отзыва пользователем
def test_user_cannot_delete_other_user_review(user, auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True)
    # получаем id отзыва
    review_id = test_review.id
    # совершаем запрос DELETE к API по URL
    review_url = reverse("product-reviews-detail", args=[review_id])
    resp = auth_client.delete(review_url)
    # проверяем код ответа,
    # должен вернуться код 403
    assert resp.status_code == HTTP_403_FORBIDDEN


''' фильтрация '''


# проверка фильтрации отзывов:
# по ID пользователя
def test_filter_review_creator_id(auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True)
    # получаем id создателя отзыва
    user_id = test_review.creator.id

    url = reverse("product-reviews-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'creator': user_id})
    assert resp.status_code == HTTP_200_OK


# проверка фильтрации отзывов:
# по дате создания
def test_filter_review_created_date(auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True)
    # получаем дату создания отзыва
    created_date = test_review.created_at

    url = reverse("product-reviews-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'created_at': created_date})
    assert resp.status_code == HTTP_200_OK


# проверка фильтрации отзывов:
# по ID товара
def test_filter_review_product_id(auth_client, review_factory):
    # создаём отзыв
    test_review = review_factory(make_m2m=True)
    # получаем id товара
    product_id = test_review.product.id
    url = reverse("product-reviews-list")
    # прописываем в URL статус, по которому будет
    # производиться фильтрация
    # совершаем запрос GET к API по URL
    resp = auth_client.get(url, {'product': product_id})
    assert resp.status_code == HTTP_200_OK
