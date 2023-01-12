from page_object.application import App


def test_first_test(desktop_app: App) -> None:
    desktop_app.login()
    desktop_app.create_test()
    desktop_app.open_test_cases()
    assert desktop_app.check_test_created()
    desktop_app.delete_test()
