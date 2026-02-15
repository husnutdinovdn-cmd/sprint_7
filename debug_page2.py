# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
BASE = "https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.set_default_timeout(15000)
    page.goto(BASE)
    page.locator('button:has-text("Заказать")').first.click()
    page.wait_for_load_state("networkidle")
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
    inputs = page.locator("input, textarea").evaluate_all("els => els.map(e => e.placeholder || e.name || '')")
    print("Inputs on step 2:", inputs)
    b.close()
