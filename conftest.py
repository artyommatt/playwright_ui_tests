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
    app = App(get_playwright)
    yield app
    app.close()
