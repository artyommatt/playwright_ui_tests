import json
import os
from typing import Generator, Dict, Any

from _pytest.fixtures import fixture
from playwright.sync_api import sync_playwright, Playwright

from page_object.application import App
from settings import BROWSER_OPTIONS


@fixture(scope="session")
def get_playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope="session")
def desktop_app(get_playwright: Playwright, request: Any) -> Generator[App, None, None]:
    base_url = request.config.getoption("--base_url")
    app = App(get_playwright, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope="session")
def desktop_app_auth(desktop_app: App, request: Any) -> Generator[App, None, None]:
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    desktop_app.goto("/login")
    desktop_app.login(**config)
    yield desktop_app


@fixture(scope="session")
def mobile_app(get_playwright: Playwright, request: Any) -> Generator[App, None, None]:
    base_url = request.config.getoption("--base_url")
    device = request.config.getoption("--device")
    app = App(get_playwright, base_url=base_url, device=device, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope="session")
def mobile_app_auth(mobile_app: App, request: Any) -> Generator[App, None, None]:
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    mobile_app.goto("/login")
    mobile_app.login(**config)
    yield desktop_app


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--secure", action="store", default="secure.json")
    parser.addoption("--device", action="store", default="")
    parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")


def load_config(config_file: str) -> Dict[str, str]:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
