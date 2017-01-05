from typing import List
from abc import ABCMeta, abstractmethod

import requests


class ProxyProvider(metaclass=ABCMeta):

    @abstractmethod
    def get_proxy_list(self) -> List[str]:
        pass


class RefreshableProxyProvider(ProxyProvider, metaclass=ABCMeta):

    @abstractmethod
    def refresh_proxy_list(self) -> None:
        pass


class ProxySpyRefreshableProxyProvider(RefreshableProxyProvider):

    def __init__(self):
        self.proxy_list = []

    @staticmethod
    def _line_contains_proxy(line: str) -> bool:
        return line[0].isdigit()

    def get_proxy_list(self) -> List[str]:
        if not self.proxy_list:
            self.refresh_proxy_list()

        return self.proxy_list

    def refresh_proxy_list(self) -> None:
        proxy_url = 'http://txt.proxyspy.net/proxy.txt'

        proxy_data = requests.get(proxy_url, timeout=10)

        for line in proxy_data.iter_lines():
            if line:
                decoded_line = line.decode(proxy_data.encoding)  # type: str
                if self._line_contains_proxy(decoded_line):
                    self.proxy_list.append(decoded_line[:decoded_line.index(' ')])

