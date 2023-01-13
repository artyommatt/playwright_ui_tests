from page_object.application import App


def test_create_test_case(desktop_app_auth: App) -> None:
    test_name = "hello"
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.test_cases.create_test(test_name, "world")
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)


def test_create_test_case_no_description(desktop_app_auth: App) -> None:
    test_name = "hello"
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.test_cases.create_test(test_name, "")
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)


def test_create_test_case_degits_name(desktop_app_auth: App) -> None:
    test_name = "123"
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.test_cases.create_test(test_name, "world")
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
