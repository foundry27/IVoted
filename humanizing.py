from typing import List, Callable
import grequests

import numpy
import time

from nonce import PageViewNonceGenerator


class Humanizer:

    def __init__(self,
                 pre_voting_actions: List[Callable[[], None]],
                 post_voting_actions: List[Callable[[], None]]):
        self.pre_voting_actions = pre_voting_actions
        self.post_voting_actions = post_voting_actions

    def perform_pre_voting_actions(self) -> None:
        for action in self.pre_voting_actions:
            action()

    def perform_post_voting_actions(self):
        for action in self.post_voting_actions:
            action()


def voting_delay_action() -> None:
    delay_time = numpy.random.choice([4, 5, 6, 7, 10, 25, 60, 60 * 10, 60 * 15],
                                     p=[0.2, 0.25, 0.2, 0.1, 0.1, 0.055, 0.05, 0.025, 0.020])

    print('Waiting {} seconds before voting again...'.format(delay_time))

    time.sleep(delay_time)


def create_view_manipulation_action(request_link: str, nonce_generator: PageViewNonceGenerator, post_id: int) -> Callable[[], None]:
    def generated():
        params = {'action': 'update_views_ajax', 'token': nonce_generator.get_page_view_nonce(), 'id': str(post_id)}

        headers = {'X-Requested-With': 'XMLHttpRequest',
                   'Connection': 'close'}
        while True:
            view_attempt = grequests.map([grequests.get(request_link, params=params, headers=headers, timeout=30)])[0]

            encoded_attempt = str(view_attempt.content, encoding=view_attempt.encoding)

            if encoded_attempt.startswith('WPP: OK'):
                print("Incremented page view count...")
                break
            else:
                print("Failed to increment page view count! Reacquiring nonce...")
                params['token'] = nonce_generator.get_page_view_nonce(refresh=True)

    return generated
