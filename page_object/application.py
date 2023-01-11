from playwright.sync_api import Playwright


class App:
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")

    def login(self):
        self.page.fill("input[name=\"username\"]", "alice")
        self.page.fill("input[name=\"password\"]", "Qamania123")
        self.page.press("input[name=\"password\"]", "Enter")

    def create_test(self):
        self.page.locator("text=Create new test").click()
        self.page.locator("input[name=\"name\"]").fill("hello")
        self.page.locator("textarea[name=\"description\"]").fill("world")
        self.page.locator("input:has-text(\"Create\")").click()

    def open_test_cases(self):
        self.page.locator("text=Test Cases").click()

    def check_test_created(self):
        return self.page.query_selector('//td[text()="hello"]') is not None

    def delete_test(self):
        self.page.locator("text=hello world alice Norun None PASS FAIL Details Delete >> button").nth(3).click()

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()