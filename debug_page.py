# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "https://9cc59b33-a48f-44c3-8f96-3ef38f5dc812.serverhub.praktikum-services.ru"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_default_timeout(20000)
    page.goto(BASE)
    page.locator('a:has-text("Заказать"), button:has-text("Заказать")').first.click()
    page.wait_for_load_state("networkidle")
    html = page.content()
    with open("order_form.html", "w", encoding="utf-8") as f:
        f.write(html)
    # All buttons and inputs
    buttons = page.locator("button, input[type=submit], a.Button").all_inner_texts()
    inputs = page.locator("input, textarea").evaluate_all("els => els.map(e => ({ placeholder: e.placeholder, name: e.name, type: e.type }))")
    print("Buttons/links:", buttons[:20])
    print("Inputs:", inputs[:15])
    browser.close()
print("Saved order_form.html")
