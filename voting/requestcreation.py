from abc import ABCMeta, abstractmethod

from grequests import AsyncRequest
from grequests import get

from rating import StarRating
from targeting import VotingTarget
from voting.voteridentity import VoterIdentity


class VotingRequestCreationService(metaclass=ABCMeta):

    @abstractmethod
    def create_request(self, target: VotingTarget, stars: StarRating, voter: VoterIdentity) -> AsyncRequest:
        pass


class ProxiedNextGENGalleryVotingRequestCreationService(VotingRequestCreationService):

    def __init__(self, voting_page_link: str):
        self.voting_page_link = voting_page_link

    def create_request(self, target: VotingTarget, stars: StarRating, voter: VoterIdentity) -> AsyncRequest:
        request_link = self.voting_page_link

        params = {'nggv_pid': target.get_target_id(),
                  'nggv_criteria_id': 0,
                  'r': stars.value,
                  'ajaxify': 1}

        headers = {'X-Requested-With': 'XMLHttpRequest',
                   'Referer': request_link,
                   'Connection': 'close'}

        proxies = {'https': 'http://' + voter.get_ip_address()}

        cookies = {'wordpress_test_cookie': 'WP+Cookie+check',
                   'wp-settings-time-1': '0'}

        return get(request_link, params=params, headers=headers, proxies=proxies, cookies=cookies, timeout=30)
