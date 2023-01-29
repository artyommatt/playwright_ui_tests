from typing import Dict, List, Tuple

from pytest import mark

from page_object.application import App

data: Dict[str, str | List[str | Tuple[str, str]]] = {
    "argnames": "name, description",
    "argvalues": [
        ("hello", "world"),
        ("hello", ""),
        ("123", "world"),
    ],
    "ids": ["general", "without description", "digit name"]
}


@mark.parametrize(**data)
def test_create_test_case(desktop_app_auth: App, name: str, description: str) -> None:
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.test_cases.create_test(name, description)
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist(name)
    desktop_app_auth.test_cases.delete_test_by_name(name)  # TODO: test-case isn't removed after raise assert


def test_testcase_does_not_exist(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Test Cases")
    assert not desktop_app_auth.test_cases.check_test_exist("not exist")
