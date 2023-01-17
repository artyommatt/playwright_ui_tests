import json
import os
from typing import Generator, Dict, Any

from _pytest.fixtures import fixture
from playwright.sync_api import sync_playwright, Playwright

from page_object.application import App


@fixture
def get_playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@fixture
def desktop_app(get_playwright: Playwright, request: Any) -> Generator[App, None, None]:
    base_url = request.config.getoption("--base_url")
    app = App(get_playwright, base_url=base_url)
    app.goto('/')
    yield app
    app.close()


@fixture
def desktop_app_auth(desktop_app: App, request: Any) -> Generator[App, None, None]:
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    desktop_app.goto("/login")
    desktop_app.login(**config)
    yield desktop_app


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")
    parser.addoption("--secure", action="store", default="secure.json")


def load_config(config_file: str) -> Dict[str, str]:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
