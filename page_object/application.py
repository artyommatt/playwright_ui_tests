from typing import Any

from playwright.sync_api import Browser

from .demo_page import DemoPages
from .test_cases import TestCases


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs: Any) -> None:
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self.page)

    def goto(self, endpoint: str, use_base_url: bool = True) -> None:
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str) -> None:
        self.page.click(f"css=header >> text=\"{menu}\"")
        self.page.wait_for_load_state()

    def login(self, login: str, password: str) -> None:
        self.page.fill("input[name=\"username\"]", login)
        self.page.fill("input[name=\"password\"]", password)
        self.page.press("input[name=\"password\"]", "Enter")

    def click_menu_btn(self) -> None:
        self.page.click(".menuBtn")

    def is_menu_btn_visible(self) -> bool:
        return self.page.is_visible(".menuBtn")

    def get_location(self) -> str | None:
        return self.page.text_content(".position")

    def close(self) -> None:
        self.page.close()
        self.context.close()
