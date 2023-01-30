from playwright.sync_api import Page


class DemoPages:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_page_after_wait(self, wait_time: int) -> None:
        self.page.fill(".waitPageTime", str(wait_time))
        with self.page.expect_navigation(wait_until="load", timeout=(wait_time + 1) * 1000):
            self.page.click(".waitPage", no_wait_after=True)

    def check_wait_page(self) -> bool:
        return "Wait Page" == self.page.text_content("h3")

    def open_page_and_wait_ajax(self, wait_time: int) -> None:
        self.page.fill(".waitAjaxRequests", str(wait_time))
        self.page.click(".waitAjax")
        self.page.wait_for_load_state("networkidle")

    def get_ajax_responses_count(self) -> int:
        return len(self.page.query_selector_all("css=.ajaxResponses > p"))

    def click_new_page_btn(self, ctrl_key: bool = False) -> None:
        if ctrl_key:
            mod = ["Control"]
        else:
            mod = None

        self.page.click(".newPage", modifiers=mod)

    def injected_js(self) -> None:
        js = '''
        console.error("this is injected error");
        alert("this is injected alert");
        '''
        self.page.evaluate(js)
