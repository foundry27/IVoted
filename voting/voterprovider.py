from abc import ABCMeta, abstractmethod
from datetime import datetime, time
from random import choice
from typing import Callable

from requests import Timeout

from voting.voteridentity import VoterIdentity, VoterPool


class VoterProvider(metaclass=ABCMeta):

    @abstractmethod
    def use_current_voter(self, voting_function: Callable[[VoterIdentity], None]) -> None:
        pass

    @abstractmethod
    def has_voters_remaining(self) -> bool:
        pass


class PooledVoterProvider(VoterProvider):

    def __init__(self, pool: VoterPool):
        self.pool = pool
        self.voter_pool = pool.generate_voter_list()
        self.current_profile = choice(self.voter_pool)
        self.previous_profile = None
        self.remaining_votes_for_voter = self.current_profile.get_max_vote_attempts()

    def refresh_voter_pool(self) -> None:
        self.voter_pool = self.pool.generate_voter_list()
        self.current_profile = choice(self.voter_pool)
        self.previous_profile = None
        self.remaining_votes_for_voter = self.current_profile.get_max_vote_attempts()

    def select_new_voter(self) -> None:
        self.previous_profile = self.current_profile
        self.current_profile = choice(self.voter_pool)
        while self.current_profile == self.previous_profile:
            self.current_profile = choice(self.voter_pool)

    def use_current_voter(self, voting_function: Callable[[VoterIdentity], None]) -> None:
        voter = self.current_profile
        self.remaining_votes_for_voter -= 1

        if self.remaining_votes_for_voter == 0:
            self.select_new_voter()

        try:
            voting_function(voter)
        except Timeout:
            print("Timed out trying to use current voter, refreshing voter pool...")
            self.refresh_voter_pool()

    def has_voters_remaining(self) -> bool:
        pass


class EndlessPooledVoterProvider(PooledVoterProvider):

    def has_voters_remaining(self) -> bool:
        return True


class BlockingDaytimeOnlyVoterProviderDecorator(VoterProvider):

    def __init__(self, backing_provider: VoterProvider):
        self.backing_provider = backing_provider

    def use_current_voter(self, voting_function: Callable[[VoterIdentity], None]) -> None:
        self.backing_provider.use_current_voter(voting_function)

    def has_voters_remaining(self) -> bool:
        if not self.backing_provider.has_voters_remaining():
            return False
        else:
            while not time(hour=8) <= datetime.now().time() <= time(hour=21):
                pass
            return self.backing_provider.has_voters_remaining()
