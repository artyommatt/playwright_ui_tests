import json

from helpers.db import DataBase
from page_object.application import App


def test_dashboard(desktop_app_auth: App) -> None:
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.navigate_to("Dashboard")
    desktop_app_auth.intercept_request("**/getstat*", payload)
    desktop_app_auth.dashboard.refresh_dashboard()
    desktop_app_auth.stop_interception("**/getstat*")
    assert desktop_app_auth.dashboard.get_total_tests_stat() == "0"


def test_multiole_roles(desktop_app_auth: App, desktop_app_bob: App, get_db: DataBase) -> None:
    alice = desktop_app_auth
    bob = desktop_app_bob
    before = alice.dashboard.get_total_tests_stat()
    bob.navigate_to('Create new test')
    bob.test_cases.create_test('test by bob', 'bob')
    alice.dashboard.refresh_dashboard()
    after = alice.dashboard.get_total_tests_stat()
    get_db.delete_test_case('test by bob')
    assert int(before) + 1 == int(after)
