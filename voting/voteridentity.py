from abc import ABCMeta, abstractmethod
from typing import List
from random import randint, choice

from proxy import RefreshableProxyProvider


class VoterIdentity:

    def __init__(self, ip_address: str, max_consecutive_vote_attempts: int):
        self.ip_address = ip_address
        self.max_consecutive_vote_attempts = max_consecutive_vote_attempts

    def get_max_vote_attempts(self) -> int:
        return self.max_consecutive_vote_attempts

    def get_ip_address(self) -> str:
        return self.ip_address


class VoterPool(metaclass=ABCMeta):

    @abstractmethod
    def generate_voter_list(self) -> List[VoterIdentity]:
        pass


class AutoUpdatingProxyVoterPool(VoterPool):

    def __init__(self, pool_size: int, proxy_provider: RefreshableProxyProvider):
        self.pool_size = pool_size
        self.proxy_provider = proxy_provider

    def generate_voter_list(self) -> List[VoterIdentity]:
        self.proxy_provider.refresh_proxy_list()
        proxies = self.proxy_provider.get_proxy_list()
        return [VoterIdentity(choice(proxies), randint(1, 15)) for i in range(1, self.pool_size)]