"""Тесты ручки «Создать заказ» (POST /api/v1/orders)."""
import allure
import pytest
import requests

from config import BASE_URL
from helpers import get_default_order_payload


@allure.feature("Orders")
@allure.story("Создание заказа")
class TestCreateOrder:
    """Тесты создания заказа."""

    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            [],
        ],
        ids=["one_color_black", "one_color_grey", "both_colors", "no_color"],
    )
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_color_parametrized(self, color):
        payload = get_default_order_payload()
        if color:
            payload["color"] = color
        else:
            payload.pop("color", None)
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201, (
            f"Ожидался код 201, получен {response.status_code}, тело: {response.text}"
        )
        body = response.json()
        assert "track" in body, f"В ответе должно быть поле track, получено: {body}"
        assert body["track"] is not None, "track не должен быть пустым"
