from page_object.application import App


def test_wait_more_30_seconds(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_after_wait(3)
    assert desktop_app_auth.demo_pages.check_wait_page()


def test_ajax(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(2)
    assert desktop_app_auth.demo_pages.get_ajax_responses_count() == 2


def test_handlers(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.click_new_page_btn()
    desktop_app_auth.demo_pages.injected_js()
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist("Check new test")
