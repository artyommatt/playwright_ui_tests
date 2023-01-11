from playwright.sync_api import expect


def test_first_test(desktop_app):
    desktop_app.login()
    desktop_app.create_test()
    desktop_app.open_test_cases()
    assert desktop_app.check_test_created()
    desktop_app.delete_test()
