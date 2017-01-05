import requests


class PageViewNonceGenerator:

    def __init__(self, view_counted_page: str):
        self.view_counted_page = view_counted_page
        self.cached_nonce = ''

    def get_page_view_nonce(self, refresh: bool = False) -> str:
        if not self.cached_nonce or refresh:
            response = requests.get(self.view_counted_page)
            response_content = str(response.content, encoding=response.encoding)
            beginning_index = response_content.find("token: \'") + len("token: \'")

            self.cached_nonce = response_content[beginning_index:beginning_index + 10]
            print("Acquired page view control nonce: {}".format(self.cached_nonce))
        return self.cached_nonce
