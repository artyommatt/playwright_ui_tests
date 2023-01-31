from typing import Dict, List, Tuple

from pytest import mark

from helpers.db import DataBase
from helpers.web_service import WebService
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


@mark.parametrize(**data)
def test_create_test_case_throw_db(desktop_app_auth: App, name: str, description: str, get_db: DataBase) -> None:
    tests = get_db.list_test_cases()
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.test_cases.create_test(name, description)
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exist(name)
    assert len(tests) + 1 == len(get_db.list_test_cases())
    get_db.delete_test_case(name)


def test_testcase_does_not_exist(desktop_app_auth: App) -> None:
    desktop_app_auth.navigate_to("Test Cases")
    assert not desktop_app_auth.test_cases.check_test_exist("not exist")


def test_delete_test_case(desktop_app_auth: App, get_web_service: WebService) -> None:
    test_name = 'test for delete'
    get_web_service.create_test(test_name, 'delete me pls')
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exist(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
    assert not desktop_app_auth.test_cases.check_test_exist(test_name)
