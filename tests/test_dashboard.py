import json

from page_object.application import App


def test_dashboard(desktop_app_auth: App) -> None:
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.navigate_to("Dashboard")
    desktop_app_auth.intercept_request("**/getstat*", payload)
    desktop_app_auth.dashboard.refresh_dashboard()
    assert desktop_app_auth.dashboard.get_total_tests_stat() == "0"
    desktop_app_auth.stop_interception("**/getstat*")
