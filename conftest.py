from typing import Generator

from _pytest.fixtures import fixture
from playwright.sync_api import sync_playwright, Playwright

from page_object.application import App


@fixture
def get_playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@fixture
def desktop_app(get_playwright: Playwright) -> Generator[App, None, None]:
    app = App(get_playwright, base_url="http://127.0.0.1:8000")
    app.goto('/')
    yield app
    app.close()


@fixture
def desktop_app_auth(desktop_app: App) -> Generator[App, None, None]:
    app = desktop_app
    app.goto("/login")
    app.login("alice", "Qamania123")
    yield app
