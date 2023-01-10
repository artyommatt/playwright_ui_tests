from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()

    page.goto("http://127.0.0.1:8000/login/?next=/")
    page.locator("input[name=\"username\"]").fill("alice")
    page.locator("input[name=\"password\"]").fill("Qamania123")

    page.locator("input[name=\"password\"]").press("Enter")
    page.locator("text=Create new test").click()
    page.locator("input[name=\"name\"]").fill("hello")
    page.locator("textarea[name=\"description\"]").fill("world")
    page.locator("input:has-text(\"Create\")").click()
    page.locator("text=Test Cases").click()

    assert page.query_selector('//td[text()="hello"]') is not None

    page.locator("text=hello world alice Norun None PASS FAIL Details Delete >> button").nth(3).click()

    # ---------------------
    page.close()
    context.close()
    browser.close()


def test_first_test():
    with sync_playwright() as playwright:
        run(playwright)
