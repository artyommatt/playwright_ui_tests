import json
import logging
import os
from typing import Generator, Dict, Any

import pytest
from _pytest.fixtures import fixture
from playwright.sync_api import sync_playwright, Playwright, Browser

from page_object.application import App


@fixture(autouse=True, scope="session")
def preconditions() -> Generator[Playwright, None, None]:
    logging.info("preconditions started")
    yield
    logging.info("postconditions started")


@fixture(scope="session")
def get_playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope="session", params=["chromium", "firefox", "webkit"], ids=["chromium", "firefox", "webkit"])
def get_browser(get_playwright: Playwright, request: Any) -> Generator[Playwright, None, None]:
    browser = request.param
    headless = request.config.getoption("--headless")
    os.environ["PWBROWSER"] = browser
    if headless == "True":
        headless = True
    else:
        headless = False

    if browser == "chromium":
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == "firefox":
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == "webkit":
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, "unsupported browser type"

    yield bro
    bro.close()
    del os.environ["PWBROWSER"]


@fixture(scope="session")
def desktop_app(get_browser: Browser, request: Any) -> Generator[App, None, None]:
    base_url = request.config.getoption("--base_url")
    app = App(get_browser, base_url=base_url)
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


@fixture(scope="session", params=["iPhone 12", "Pixel 5"])
def mobile_app(get_playwright: Playwright, get_browser: Browser, request: Any) -> Generator[App, None, None]:
    if os.environ.get("PWBROWSER") == "firefox":
        pytest.skip()
    base_url = request.config.getoption("--base_url")
    device = request.config.getoption("--device")
    device_config = get_playwright.devices.get(device)
    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope="session")
def mobile_app_auth(mobile_app: App, request: Any) -> Generator[App, None, None]:
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    mobile_app.goto("/login")
    mobile_app.login(**config)
    yield mobile_app


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--secure", action="store", default="secure.json")
    parser.addoption("--device", action="store", default="")
    parser.addoption("--browser", action="store", default="chromium")
    parser.addoption("--base_url", action="store", default="http://127.0.0.1:8000")
    parser.addoption("--headless", action="store", help="run tests with headless", default="True")


def load_config(config_file: str) -> Dict[str, str]:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
