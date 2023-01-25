from page_object.application import App


def test_location_ok(desktop_app_auth: App) -> None:
    assert "48.8:2.3" == desktop_app_auth.get_location()
