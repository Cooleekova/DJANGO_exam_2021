import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK


# проверка получения списка отзывов
@pytest.mark.django_db
def test_collection_list(client, review_factory):
    # создаём десять отзывов
    review = review_factory(_quantity=10)
    url = reverse("product-reviews-list")
    # совершаем запрос GET к API по URL
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json
    # проверяем, что вернувшийся json содержит десять записей
    assert len(resp_json) == 10




