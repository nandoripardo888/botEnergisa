from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()
    pagina.goto("https://aec.testing.sambatech.dev/")
    pagina.locator(
        'xpath=/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]/button[1]/span[1]').click()
    pagina.fill(
        'xpath=/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/input[1]', "226288")
    pagina.fill(
        'xpath=/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/form[1]/div[1]/div[2]/div[1]/input[1]', "123456")
    pagina.locator(
        'xpath=//*[@id="sidebar-login"]/div[1]/div/form/div[1]/div[3]/select').click()

    pagina.locator(
        'xpath=//*[@id="sidebar-login"]/div[1]/div/form/div[1]/div[3]/select').click()
    time.sleep(15)
    print("terminou tempo")
    pagina.locator(
        '#sidebar-login > div:nth-child(1) > div > form > div:nth-child(1) > div.affiliates > select > option:nth-child(2)').click()

    # time.sleep(5)
