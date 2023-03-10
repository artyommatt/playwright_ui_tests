import logging
from typing import Any

from playwright.sync_api import Browser, Route, Request, ConsoleMessage, Dialog

from .dashboard import Dashboard
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
        self.dashboard = Dashboard(self.page)

        def console_handler(message: ConsoleMessage) -> None:
            if message.type == "error":
                logging.error(f"page: {self.page.url}, console error: {message.text}")

        def dialog_handler(dialog: Dialog) -> None:
            logging.warning(f"page: {self.page.url}, dialog text: {dialog.message}")
            dialog.accept()

        self.page.on("console", console_handler)
        self.page.on("dialog", dialog_handler)

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

    def intercept_request(self, url: str, payload: str) -> None:
        def handler(route: Route, request: Request) -> None:
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)

    def stop_interception(self, url: str) -> None:
        self.page.unroute(url)

    def close(self) -> None:
        self.page.close()
        self.context.close()
