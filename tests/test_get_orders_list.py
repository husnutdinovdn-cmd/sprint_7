"""Тесты ручки «Получение списка заказов» (GET /api/v1/orders)."""
import allure
import requests

from config import BASE_URL


@allure.feature("Orders")
@allure.story("Список заказов")
class TestGetOrdersList:
    """Тесты получения списка заказов."""

    @allure.title("В теле ответа возвращается список заказов")
    def test_get_orders_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        body = response.json()
        assert "orders" in body, "В ответе должно быть поле orders"
        assert isinstance(body["orders"], list), (
            f"orders должен быть списком (list), получен тип: {type(body['orders'])}"
        )
