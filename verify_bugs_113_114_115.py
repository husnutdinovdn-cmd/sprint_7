# -*- coding: utf-8 -*-
"""
Проверка bug-113, bug-114, bug-115 на тестовом стенде веб-приложения.
Селекторы по реальной странице: кнопка "Далее", placeholder "* Имя" и т.д.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

BASE = "https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru"

def run():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE)
            page.locator('button:has-text("Заказать")').first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

            # Закрыть куки если есть
            cookie_btn = page.locator('button:has-text("да все привыкли")')
            if cookie_btn.count() > 0:
                cookie_btn.click()
                page.wait_for_timeout(300)

            # --- bug-113: ввод "Неизвестная" в станцию метро, нажать Далее ---
            try:
                page.get_by_placeholder("* Имя").fill("Иван")
                page.get_by_placeholder("* Фамилия").fill("Иванов")
                page.get_by_placeholder("* Адрес").fill("ул. Ленина, д. 1")
                metro = page.locator('.select-search__input, input[placeholder*="Станция метро"]').first
                metro.fill("Неизвестная")
                page.wait_for_timeout(800)
                page.get_by_placeholder("* Телефон").fill("+79001234567")
                page.wait_for_timeout(300)
                btn_dalee = page.locator('button:has-text("Далее")').first
                btn_dalee.click()
                page.wait_for_timeout(1500)
                # Проверяем: перешли на вторую страницу? Есть текст "Когда привезти" или "Про аренду"?
                on_second = page.locator('text=Когда привезти, text=Про аренду').count() > 0
                # Есть ли видимая ошибка под полем метро или общая?
                err_visible = page.locator('.Input_ErrorMessage__3HvIb:visible, [class*="Error"]:visible').count() > 0
                results["bug-113"] = {
                    "reproduced": on_second and not err_visible,
                    "detail": "Введено «Неизвестная» в станцию метро. Переход на вторую страницу без ошибки — баг воспроизведён." if (on_second and not err_visible) else "Ошибка отображается или переход заблокирован."
                }
            except Exception as e:
                results["bug-113"] = {"reproduced": None, "detail": str(e)[:200]}

            # --- bug-114: на второй странице поле даты пустое, кнопка «Заказать» активна? ---
            try:
                page.goto(BASE)
                page.locator('button:has-text("Заказать")').first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(500)
                if page.locator('button:has-text("да все привыкли")').count() > 0:
                    page.locator('button:has-text("да все привыкли")').click()
                    page.wait_for_timeout(300)
                page.get_by_placeholder("* Имя").fill("Иван")
                page.get_by_placeholder("* Фамилия").fill("Иванов")
                page.get_by_placeholder("* Адрес").fill("ул. Ленина, д. 1")
                metro = page.locator('.select-search__input').first
                metro.click()
                page.wait_for_timeout(600)
                # Клик по первому варианту в выпадающем списке метро
                first_station = page.locator('.select-search__option, li, [role="option"]').first
                if first_station.count() > 0:
                    first_station.click()
                page.wait_for_timeout(300)
                page.get_by_placeholder("* Телефон").fill("+79001234567")
                page.locator('button:has-text("Далее")').first.click()
                page.wait_for_timeout(1500)
                # На второй странице: не заполняем дату, проверяем кнопку «Заказать»
                order_btn = page.locator('button:has-text("Заказать")').filter(has=page.locator('xpath=..')).first
                if page.locator('text=Про аренду').count() == 0:
                    order_btn = page.locator('button:has-text("Заказать")').nth(1) if page.locator('button:has-text("Заказать")').count() > 1 else page.locator('button:has-text("Заказать")').first
                else:
                    order_btn = page.locator('button:has-text("Заказать")').first
                order_btn_visible = order_btn.count() > 0
                disabled = True
                if order_btn_visible:
                    try:
                        disabled = order_btn.is_disabled()
                    except Exception:
                        disabled = False
                results["bug-114"] = {
                    "reproduced": order_btn_visible and not disabled,
                    "detail": "Поле даты пустое. Кнопка «Заказать» активна (не заблокирована) — баг воспроизведён." if (order_btn_visible and not disabled) else "Кнопка заблокирована или не найдена."
                }
            except Exception as e:
                results["bug-114"] = {"reproduced": None, "detail": str(e)[:200]}

            # --- bug-115: комментарий 24 символа — подсветка; 25-й символ ---
            try:
                page.goto(BASE)
                page.locator('button:has-text("Заказать")').first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(500)
                if page.locator('button:has-text("да все привыкли")').count() > 0:
                    page.locator('button:has-text("да все привыкли")').click()
                    page.wait_for_timeout(300)
                page.get_by_placeholder("* Имя").fill("Иван")
                page.get_by_placeholder("* Фамилия").fill("Иванов")
                page.get_by_placeholder("* Адрес").fill("ул. Ленина, д. 1")
                page.locator('.select-search__input').first.click()
                page.wait_for_timeout(600)
                page.locator('.select-search__option, li').first.click()
                page.wait_for_timeout(200)
                page.get_by_placeholder("* Телефон").fill("+79001234567")
                page.locator('button:has-text("Далее")').first.click()
                page.wait_for_timeout(1500)
                # Вторая страница: дата, срок аренды — заполняем минимально, потом комментарий
                date_inp = page.locator('input[placeholder*="ривез"], input').first
                date_inp.click()
                page.wait_for_timeout(700)
                # Клик по любой дате в календаре (не сегодня)
                day_btn = page.locator('button, [class*="day"]').filter(has_not_text="").nth(10)
                if day_btn.count() > 0:
                    day_btn.click()
                page.wait_for_timeout(400)
                comment_24 = "а" * 24
                comment_inp = page.get_by_placeholder("Комментарий")
                if comment_inp.count() == 0:
                    comment_inp = page.locator('textarea').first
                comment_inp.fill(comment_24)
                page.wait_for_timeout(500)
                parent = comment_inp.locator('xpath=..')
                has_error_class = page.locator('.Input_ErrorMessage__3HvIb').count() > 0 or 'error' in (comment_inp.get_attribute('class') or '')
                comment_inp.press('b')
                page.wait_for_timeout(300)
                val = comment_inp.input_value() if comment_inp.evaluate('el => el.tagName') == 'TEXTAREA' else (comment_inp.get_attribute('value') or '')
                try:
                    val = page.evaluate('() => document.querySelector("textarea")?.value || document.querySelector("input[placeholder*=\\"Комментарий\\"]")?.value || ""')
                except Exception:
                    pass
                len_after = len(val)
                results["bug-115"] = {
                    "reproduced": not has_error_class and len_after <= 24,
                    "detail": f"Введено 24 символа. Подсветка ошибки: {has_error_class}. Длина после попытки 25-го: {len_after}. Ожидалось: красная подсветка при 24, блок 25-го."
                }
            except Exception as e:
                results["bug-115"] = {"reproduced": None, "detail": str(e)[:200]}

        finally:
            browser.close()

    return results

if __name__ == "__main__":
    r = run()
    for bid, data in r.items():
        print(f"{bid}: reproduced={data['reproduced']}, detail={data['detail']}")
