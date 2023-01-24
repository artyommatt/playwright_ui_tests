from page_object.application import App


def test_test_cases_columns_hidden(mobile_app_auth: App) -> None:
    mobile_app_auth.click_menu_btn()
    mobile_app_auth.navigate_to("Test Cases")
    assert mobile_app_auth.test_cases.check_columns_hidden_in_mobile()
