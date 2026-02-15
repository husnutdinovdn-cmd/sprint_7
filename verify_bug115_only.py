# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
BASE = "https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.set_default_timeout(20000)
    page.goto(BASE)
    page.locator('button:has-text("Заказать")').first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    if page.locator('button:has-text("да все привыкли")').count() > 0:
        page.locator('button:has-text("да все привыкли")').click()
    page.get_by_placeholder("* Имя").fill("Иван")
    page.get_by_placeholder("* Фамилия").fill("Иванов")
    page.get_by_placeholder("* Адрес").fill("ул. Ленина, 1")
    page.locator('.select-search__input').first.click()
    page.wait_for_timeout(600)
    page.locator('.select-search__option').first.click()
    page.get_by_placeholder("* Телефон").fill("+79001234567")
    page.locator('button:has-text("Далее")').first.click()
    page.wait_for_timeout(2000)
    # Дата: клик и выбор (любой день)
    page.get_by_placeholder("* Когда привезти самокат").click()
    page.wait_for_timeout(800)
    page.locator('.react-datepicker__day').first.click()
    page.wait_for_timeout(400)
    # Комментарий 24 символа
    comment_inp = page.get_by_placeholder("Комментарий для курьера")
    comment_24 = "а" * 24
    comment_inp.fill(comment_24)
    page.wait_for_timeout(600)
    # Есть ли красная подсветка (класс ошибки у родителя или у поля)?
    err_msg = page.locator('.Input_ErrorMessage__3HvIb').filter(has=page.locator('xpath=..'))
    parent = comment_inp.locator('xpath=..')
    has_red = 'Input_Responsible' in (parent.get_attribute('class') or '') or page.locator('.Input_ErrorMessage__3HvIb').count() > 0
    comment_inp.press('b')
    page.wait_for_timeout(400)
    val = comment_inp.input_value()
    len_after = len(val)
    print("bug-115: has_error_class=", has_red, "len_after=", len_after, "reproduced=", (not has_red and len_after <= 24))
    b.close()
