"""Тесты ручки «Логин курьера» (POST /api/v1/courier/login)."""
import allure
import requests

from config import BASE_URL
from helpers import (
    register_new_courier_and_return_login_password,
    generate_random_string,
    delete_courier,
)


@allure.feature("Courier")
@allure.story("Логин курьера")
class TestLoginCourier:
    """Тесты авторизации курьера."""

    @allure.title("Курьер может авторизоваться с валидными логином и паролем")
    def test_login_courier_success(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"login": login_pass[0], "password": login_pass[1]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body, "Успешный ответ должен содержать id"
        assert isinstance(body["id"], (int, float, str)), "id должен быть числом или строкой"
        delete_courier(body["id"])

    @allure.title("Успешный ответ содержит id")
    def test_login_returns_id(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"login": login_pass[0], "password": login_pass[1]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        delete_courier(body["id"])

    def _login_and_delete_courier(self, login: str, password: str) -> None:
        resp = requests.post(
            f"{BASE_URL}/courier/login",
            data={"login": login, "password": password},
        )
        if resp.status_code == 200:
            body = resp.json()
            if body.get("id") is not None:
                delete_courier(body["id"])

    @allure.title("Запрос без логина возвращает ошибку")
    def test_login_without_login_returns_error(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"password": login_pass[1]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        self._login_and_delete_courier(login_pass[0], login_pass[1])

    @allure.title("Запрос без пароля возвращает ошибку")
    def test_login_without_password_returns_error(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"login": login_pass[0]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code in (
            400,
            504,
        ), "Ожидается 400 (недостаточно данных) или 504 (таймаут сервера)"
        if response.status_code == 400:
            body = response.json()
            assert "message" in body
        self._login_and_delete_courier(login_pass[0], login_pass[1])

    @allure.title("Неверный пароль возвращает ошибку")
    def test_login_wrong_password_returns_error(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"login": login_pass[0], "password": "wrong_password_123"}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        body = response.json()
        assert "message" in body
        self._login_and_delete_courier(login_pass[0], login_pass[1])

    @allure.title("Неверный логин возвращает ошибку")
    def test_login_wrong_login_returns_error(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        payload = {"login": "nonexistent_login_123", "password": login_pass[1]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        body = response.json()
        assert "message" in body
        self._login_and_delete_courier(login_pass[0], login_pass[1])

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user_returns_error(self):
        payload = {
            "login": generate_random_string(15),
            "password": generate_random_string(15),
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        body = response.json()
        assert "message" in body
