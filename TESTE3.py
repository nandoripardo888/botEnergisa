from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe")
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://fast.com/pt/")
    page.screenshot(path=f"example.png")