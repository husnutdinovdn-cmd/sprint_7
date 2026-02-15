# Sprint_7 — тесты API Scooter

Тесты для API сервиса доставки самокатов (qa-scooter.praktikum-services.ru).

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest
```

## Генерация отчёта Allure

1. Запустить тесты (результаты сохраняются в `allure-results/`):

   ```bash
   pytest
   ```

2. Сгенерировать и открыть отчёт:

   ```bash
   allure serve allure-results
   ```

   Или только сгенерировать отчёт в папку `allure-report/`:

   ```bash
   allure generate allure-results -o allure-report --clean
   ```

Для работы `allure serve` / `allure generate` нужна установленная [Allure Commandline](https://docs.qameta.io/allure/#_installing_a_commandline).

## Структура

- `config.py` — базовый URL API
- `helpers.py` — регистрация курьера, удаление, данные заказа
- `tests/test_create_courier.py` — создание курьера
- `tests/test_login_courier.py` — логин курьера
- `tests/test_create_order.py` — создание заказа (параметризация по цветам)
- `tests/test_get_orders_list.py` — список заказов
