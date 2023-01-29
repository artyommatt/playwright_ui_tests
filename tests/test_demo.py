from page_object.application import App


def test_wait_more_30_seconds(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_after_wait(32)
    assert desktop_app_auth.demo_pages.check_wait_page()


def test_ajax(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(6)
    assert desktop_app_auth.demo_pages.get_ajax_responses_count() == 6
