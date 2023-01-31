from playwright.sync_api import Page


class Dashboard:
    def __init__(self, page: Page) -> None:
        self.page = page

    def refresh_dashboard(self) -> None:
        self.page.click("input")
        self.page.wait_for_event('response')

    def get_total_tests_stat(self) -> str:
        return self.page.text_content(".total >> span")
