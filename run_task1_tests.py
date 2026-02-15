# -*- coding: utf-8 -*-
"""
Тестирование API тестового стенда и обновление Excel с результатами (PASSED/FAILED).
Стенд: https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru
"""
import requests
import openpyxl

BASE_URL = "https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru/api/v1"
EXCEL_PATH = r'D:\Иван Иванов — диплом_Инженер по тестированию-v-2-4-25.xlsx'

def create_order(payload=None):
    if payload is None:
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Ленина, д. 1",
            "metroStation": 4,
            "phone": "+79001234567",
            "rentTime": 3,
            "deliveryDate": "2025-02-20",
            "comment": "Тест",
        }
    r = requests.post(f"{BASE_URL}/orders", json=payload, timeout=10)
    return r

def get_order_by_track(track):
    r = requests.get(f"{BASE_URL}/orders/track", params={"t": track}, timeout=10)
    return r

def cancel_order(track):
    r = requests.put(f"{BASE_URL}/orders/cancel", params={"track": track}, timeout=10)
    return r

def run_api_checks():
    results = {"order_create": None, "order_get_track": None, "order_cancel": None}
    track = None
    # 1. Создание заказа
    resp = create_order()
    results["order_create"] = "PASSED" if (resp.status_code == 201 and resp.json().get("track")) else "FAILED"
    if resp.status_code == 201:
        track = resp.json().get("track")
    # 2. Получение заказа по track
    if track:
        resp2 = get_order_by_track(track)
        results["order_get_track"] = "PASSED" if resp2.status_code == 200 else "FAILED"
    else:
        results["order_get_track"] = "FAILED"
    # 3. Отмена заказа
    if track:
        resp3 = cancel_order(track)
        results["order_cancel"] = "PASSED" if resp3.status_code == 200 else "FAILED"
    else:
        results["order_cancel"] = "FAILED"
    return results

def run_validation_checks():
    """Проверки валидации через API (бэкенд)."""
    results = []
    # Невалидное имя (1 символ)
    r = create_order(get_default_payload(firstName="А"))
    results.append(("Имя 1 символ", "FAILED" if r.status_code == 201 else "PASSED"))
    # Невалидное имя (латиница)
    r = create_order(get_default_payload(firstName="John"))
    results.append(("Имя латиница", "FAILED" if r.status_code == 201 else "PASSED"))
    # Невалидный телефон
    r = create_order(get_default_payload(phone="123"))
    results.append(("Телефон короткий", "FAILED" if r.status_code == 201 else "PASSED"))
    # Несуществующий track
    r = get_order_by_track(999999)
    results.append(("Неверный номер заказа", "PASSED" if r.status_code == 404 or (r.status_code == 200 and not r.json().get("order")) else "FAILED"))
    return results

def get_default_payload(**kw):
    p = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Ленина, д. 1",
        "metroStation": 4,
        "phone": "+79001234567",
        "rentTime": 3,
        "deliveryDate": "2025-02-20",
        "comment": "Тест",
    }
    p.update(kw)
    return p

if __name__ == "__main__":
    print("Running API checks...")
    res = run_api_checks()
    for k, v in res.items():
        print(k, v)
    print("Validation (backend)...")
    for name, status in run_validation_checks():
        print(name, status)
