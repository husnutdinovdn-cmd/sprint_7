"""Вспомогательные функции для тестов API Scooter."""
import requests
import random
import string

from config import BASE_URL


def generate_random_string(length: int) -> str:
    """Генерирует строку из букв нижнего регистра заданной длины."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает [login, password, first_name].
    При неудачной регистрации возвращает пустой список.
    """
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }
    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        login_pass.extend([login, password, first_name])
    return login_pass


def delete_courier(courier_id: int) -> requests.Response:
    """Удаляет курьера по id. Используется для очистки после тестов."""
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


def get_default_order_payload(**overrides):
    """Возвращает тело заказа по умолчанию. Можно переопределить поля через overrides."""
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }
    payload.update(overrides)
    return payload
