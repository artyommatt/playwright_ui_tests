from playwright.sync_api import Page


class TestCases:
    def __init__(self, page: Page) -> None:
        self.page = page

    def create_test(self, test_name: str, test_description: str) -> None:
        self.page.fill("input[name=\"name\"]", test_name)
        self.page.fill("textarea[name=\"description\"]", test_description)
        self.page.click("input:has-text(\"Create\")")

    def check_test_exist(self, test_name: str) -> bool:
        return self.page.query_selector(f"css=tr >> text=\"{test_name}\"") is not None

    def delete_test_by_name(self, test_name: str) -> None:
        row = self.page.query_selector(f"*css=tr >> text=\"{test_name}\"")
        row.query_selector(".deleteBtn").click()

    def check_columns_hidden_in_mobile(self) -> bool:
        description = self.page.is_hidden(".thDes")
        author = self.page.is_hidden(".thAuthor")
        executor = self.page.is_hidden(".thLast")
        return description and author and executor
